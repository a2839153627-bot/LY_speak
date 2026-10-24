#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sherpa TTS节点：调用Sherpa本地语音合成模型，生成并播放TTS语音。"""

from __future__ import annotations

import importlib.util
import json
import os
import queue
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time
import wave
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Optional

import numpy as np
import rclpy
from insp_interfaces.srv import Speak
from rclpy.node import Node
from std_msgs.msg import String


DIGITS = {"0": "零", "1": "一", "2": "二", "3": "三", "4": "四",
          "5": "五", "6": "六", "7": "七", "8": "八", "9": "九"}
SENTENCE_PUNCT = "，。！？；、,.!?;"
DROP_PUNCT = set(
    "：:（）()【】[]{}《》<>“”\"‘’'`·~～@#￥$%^&*_+=|\\/—-"
)


def _num_to_chinese(num_str: str) -> str:
    num_str = str(num_str or "").strip()
    if not num_str:
        return ""
    num_str = num_str.lstrip("0") or "0"
    if len(num_str) == 1:
        return DIGITS[num_str]
    n = int(num_str)
    if n == 0:
        return "零"
    if 10 <= n < 20:
        return "十" + (DIGITS[num_str[-1]] if num_str[-1] != "0" else "")
    units = ["", "十", "百", "千", "万", "十万", "百万", "千万", "亿"]
    if len(num_str) > len(units):
        return "".join(DIGITS.get(d, d) for d in num_str)
    result = []
    digits = list(num_str)
    length = len(digits)
    for idx, d in enumerate(digits):
        if d == "0":
            if idx < length - 1 and digits[idx + 1] != "0":
                result.append("零")
            continue
        pos = length - 1 - idx
        result.append(DIGITS[d])
        if pos > 0:
            result.append(units[pos])
    return "".join(result)


def _convert_digits(text: str) -> str:
    result = []
    i = 0
    while i < len(text):
        if text[i].isdigit():
            start = i
            while i < len(text) and text[i].isdigit():
                i += 1
            has_decimal = False
            if i < len(text) and text[i] == "." and i + 1 < len(text) and text[i + 1].isdigit():
                has_decimal = True
                i += 1
                while i < len(text) and text[i].isdigit():
                    i += 1
            num_str = text[start:i]
            if has_decimal:
                int_part, dec_part = num_str.split(".")
                result.append(_num_to_chinese(int_part))
                result.append("点")
                for d in dec_part:
                    result.append(DIGITS[d])
            else:
                result.append(_num_to_chinese(num_str))
        else:
            result.append(text[i])
            i += 1
    return "".join(result)


def _normalize_tts_text(text: str) -> str:
    text = _convert_digits(str(text or ""))
    result = []
    last_space = False
    for ch in text:
        if ch.isspace() or ch in SENTENCE_PUNCT or ch in DROP_PUNCT:
            if result and not last_space:
                result.append(" ")
                last_space = True
            continue
        result.append(ch)
        last_space = False
    return re.sub(r"\s+", " ", "".join(result)).strip()


def _load_tts_sherpa_module(sherpa_dir: str):
    module_path = Path(sherpa_dir).expanduser().resolve() / "tts_sherpa.py"
    if not module_path.is_file():
        raise FileNotFoundError(f"tts_sherpa.py not found: {module_path}")
    spec = importlib.util.spec_from_file_location("local_tts_sherpa", str(module_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load tts_sherpa.py: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["local_tts_sherpa"] = module
    spec.loader.exec_module(module)
    return module


def _write_wav(path: str, samples: np.ndarray, sample_rate: int) -> None:
    pcm = np.clip(samples, -1.0, 1.0)
    pcm16 = (pcm * 32767.0).astype(np.int16)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(int(sample_rate))
        wf.writeframes(pcm16.tobytes())


class SherpaTtsNode(Node):
    def __init__(self) -> None:
        super().__init__("sherpa_tts_node")

        self.declare_parameter("sherpa_dir", str(Path.home() / "voiceModel" / "sherpa"))
        self.declare_parameter(
            "model_dir",
            str(Path.home() / "voiceModel" / "sherpa" / "matcha-icefall-zh-en"),
        )
        self.declare_parameter(
            "vocoder",
            str(Path.home() / "voiceModel" / "sherpa" / "vocos-16khz-univ.onnx"),
        )
        self.declare_parameter("provider", "cpu")
        self.declare_parameter("num_threads", 2)
        self.declare_parameter("speed", 1.0)
        self.declare_parameter("sid", 0)
        self.declare_parameter("tail_silence_ms", 250)
        self.declare_parameter("player", "aplay")
        self.declare_parameter("audio_device", "")
        self.declare_parameter("status_topic", "/tts/status")
        self.declare_parameter("progress_topic", "/inspection_progress_json")
        self.declare_parameter("auto_progress", False)
        self.declare_parameter("min_interval_sec", 1.5)
        self.declare_parameter("replace_pending", True)
        self.declare_parameter("model_type", "matcha")
        self.declare_parameter("noise_scale", 1.0)
        self.declare_parameter("length_scale", 1.0)

        self._speech_queue: queue.Queue[tuple[int, str]] = queue.Queue(maxsize=16)
        self._last_spoken_key = ""
        self._last_spoken_ts = 0.0
        self._closed = False
        self._state_lock = threading.Lock()
        self._generation = 0
        self._player_proc: Optional[subprocess.Popen] = None

        sherpa_dir = str(self.get_parameter("sherpa_dir").value)
        module = _load_tts_sherpa_module(sherpa_dir)
        args = SimpleNamespace(
            model_dir=str(self.get_parameter("model_dir").value),
            acoustic_model=None,
            vocoder=str(self.get_parameter("vocoder").value),
            provider=str(self.get_parameter("provider").value),
            num_threads=int(self.get_parameter("num_threads").value),
            max_num_sentences=1,
            debug=False,
            model_type=str(self.get_parameter("model_type").value),
            noise_scale=float(self.get_parameter("noise_scale").value),
            length_scale=float(self.get_parameter("length_scale").value),
        )

        self.get_logger().info("loading sherpa tts model...")
        self._tts = module.build_tts(args)
        self.get_logger().info("sherpa tts ready")

        status_topic = str(self.get_parameter("status_topic").value)
        progress_topic = str(self.get_parameter("progress_topic").value)
        self._status_pub = self.create_publisher(String, status_topic, 10)
        self._speak_srv = self.create_service(Speak, "/voice/speak", self._on_speak)
        self.create_subscription(String, progress_topic, self._on_progress, 10)

        self._worker = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker.start()

    def _on_say(self, msg: String) -> None:
        text = _normalize_tts_text(msg.data)
        if text:
            self._enqueue(text)

    def _on_speak(self, request, response):
        text = _normalize_tts_text(request.text)
        if not text:
            response.accepted = False
            response.message = "empty text"
            return response
        self._enqueue(text)
        response.accepted = True
        response.message = "queued"
        return response

    def _on_progress(self, msg: String) -> None:
        if not bool(self.get_parameter("auto_progress").value):
            return
        try:
            payload = json.loads(msg.data or "{}")
        except Exception:
            return
        text = self._progress_to_text(payload)
        if text:
            self._enqueue(text, key=self._progress_key(payload))

    def _progress_key(self, payload: dict[str, Any]) -> str:
        return "|".join(
            [
                str(payload.get("task_id", "")),
                str(payload.get("point_id", "")),
                str(payload.get("step", "")),
                str(payload.get("nav_status", "")),
            ]
        )

    def _progress_to_text(self, payload: dict[str, Any]) -> str:
        step = str(payload.get("step", "") or "").strip()
        point_name = str(payload.get("point_name", "") or "").strip()
        remark = str(payload.get("remark", "") or "").strip()

        if step == "downloaded":
            return remark or "已获取到最新巡检任务。"
        if step == "localizing":
            return "正在进行自动定位。"
        if step == "localized":
            return "自动定位完成，现在开始巡检。"
        if step == "localization_failed":
            return "自动定位失败，请检查机器人当前位置。"
        if step == "navigating":
            return f"正在前往{point_name}。" if point_name else "正在前往下一个巡检点。"
        if step == "arrived":
            return f"已到达{point_name}。" if point_name else "已到达巡检点。"
        if step == "navigation_failed":
            return "前方通道可能被遮挡，请让开通道。"
        if step == "recognition_failed":
            return f"{point_name}识别失败。" if point_name else "识别失败。"
        if step == "finished":
            return remark or "巡检任务已完成。"
        if step == "uploaded":
            return "巡检结果已上传完成。"
        if step == "failed":
            return remark or "巡检任务执行失败。"
        return ""

    def _enqueue(self, text: str, key: Optional[str] = None) -> None:
        now = time.time()
        dedupe_key = key or text
        min_interval = float(self.get_parameter("min_interval_sec").value)
        if dedupe_key == self._last_spoken_key and now - self._last_spoken_ts < min_interval:
            return

        replace_pending = bool(self.get_parameter("replace_pending").value)
        if replace_pending:
            while True:
                try:
                    self._speech_queue.get_nowait()
                except queue.Empty:
                    break

        try:
            with self._state_lock:
                self._generation += 1
                generation = self._generation
            self._interrupt_player()
            self._speech_queue.put_nowait((generation, text))
            self._last_spoken_key = dedupe_key
            self._last_spoken_ts = now
        except queue.Full:
            self.get_logger().warning("tts queue is full, dropping message")

    def _worker_loop(self) -> None:
        while not self._closed and rclpy.ok():
            try:
                generation, text = self._speech_queue.get(timeout=0.2)
            except queue.Empty:
                continue
            try:
                self._speak(generation, text)
            except Exception as exc:
                self.get_logger().error(f"tts speak failed: {exc}")
                self._publish_status("error", text, generation)

    def _publish_status(self, state: str, text: str = "", generation: int = 0) -> None:
        payload = {
            "state": state,
            "text": text,
            "generation": generation,
            "timestamp": int(time.time() * 1000),
        }
        msg = String()
        msg.data = json.dumps(payload, ensure_ascii=False)
        self._status_pub.publish(msg)

    def _is_current(self, generation: int) -> bool:
        with self._state_lock:
            return generation == self._generation

    def _interrupt_player(self) -> None:
        with self._state_lock:
            proc = self._player_proc
        if proc is None or proc.poll() is not None:
            return
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except Exception:
            try:
                proc.terminate()
            except Exception:
                pass

    def _speak(self, generation: int, text: str) -> None:
        speed = float(self.get_parameter("speed").value)
        sid = int(self.get_parameter("sid").value)
        tail_silence_ms = int(self.get_parameter("tail_silence_ms").value)
        original_text = str(text or "")
        text = _normalize_tts_text(text)
        if not text:
            return
        audio = self._tts.generate(text, sid=sid, speed=speed)
        if not self._is_current(generation):
            return
        samples = np.asarray(audio.samples, dtype=np.float32)
        if tail_silence_ms > 0:
            tail_samples = int(audio.sample_rate * tail_silence_ms / 1000)
            samples = np.concatenate([samples, np.zeros(tail_samples, dtype=samples.dtype)])

        fd, wav_path = tempfile.mkstemp(prefix="sherpa_tts_", suffix=".wav")
        os.close(fd)
        started = False
        interrupted = False
        try:
            _write_wav(wav_path, samples, int(audio.sample_rate))
            cmd = [str(self.get_parameter("player").value)]
            audio_device = str(self.get_parameter("audio_device").value).strip()
            if cmd[0] == "aplay" and audio_device:
                cmd += ["-D", audio_device]
            cmd.append(wav_path)
            self.get_logger().info(f"say: {text}")
            proc = subprocess.Popen(cmd, start_new_session=True)
            started = True
            self._publish_status("start", original_text, generation)
            with self._state_lock:
                self._player_proc = proc
            while proc.poll() is None:
                if not self._is_current(generation):
                    interrupted = True
                    self._interrupt_player()
                    break
                time.sleep(0.05)
            try:
                proc.wait(timeout=1.0)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except Exception:
                    proc.kill()
        finally:
            with self._state_lock:
                if self._player_proc is not None and self._player_proc.poll() is not None:
                    self._player_proc = None
            if started:
                self._publish_status("interrupted" if interrupted else "end", original_text, generation)
            try:
                os.remove(wav_path)
            except OSError:
                pass

    def destroy_node(self) -> bool:
        self._closed = True
        self._interrupt_player()
        return super().destroy_node()


def main(args=None) -> None:
    rclpy.init(args=args)
    node = SherpaTtsNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
