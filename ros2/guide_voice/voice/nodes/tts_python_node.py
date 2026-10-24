"""Python TTS节点：使用本地ONNX模型把文本合成为语音并播放。

本副本属于 LY_Guide 讲解任务（LY_speak_ws），与巡检（LY_inspect_ws）的语音
服务相互独立：节点名 guide_tts_node、服务 /guide_voice/speak、状态话题
/guide_tts/status。模型文件（~/voiceModel）与音频缓存目录沿用原路径，
两套服务只读共享，互不影响。
"""

import hashlib
import os, time, json, queue, threading, subprocess, tempfile, wave, signal, re
from pathlib import Path
import numpy as np
import onnxruntime as ort
import rclpy
from insp_interfaces.srv import Speak
from rclpy.node import Node
from std_msgs.msg import String
from pypinyin import pinyin, Style
from scipy import signal as scisig


MODEL_DIR = os.environ.get(
    "SMART_ROBOT_TTS_MODEL_DIR",
    str(Path.home() / "voiceModel" / "sherpa" / "matcha-icefall-zh-en"),
)
VOCAB_PATH = os.path.join(MODEL_DIR, "tokens.txt")
LEXICON_PATH = os.path.join(MODEL_DIR, "lexicon.txt")
ACOUSTIC_PATH = os.path.join(MODEL_DIR, "model-steps-6.onnx")
VOCODER_PATH = os.environ.get(
    "SMART_ROBOT_TTS_VOCODER_PATH",
    str(Path.home() / "voiceModel" / "sherpa" / "vocos-16khz-univ.onnx"),
)
TARGET_RMS = 0.15
DEDUP_INTERVAL = 1.5
QUEUE_MAXSIZE = 16
MAX_TTS_CHARS = 80
# 讲解任务没有巡检那套固定播报短语，不启用永久缓存：讲解词走 guide 缓存
# 目录（前端预生成），其他动态播报合成后用完即删。
# 注意：这个默认值必须是 []，且配置 yaml 里绝不能写 "persistent_cache_texts: []"——
# ROS2 的 yaml 参数解析会把空数组当成"参数未设置"，反而盖掉这里的默认值，
# 节点启动直接抛 ParameterUninitializedException（2026-10-24 真机踩坑）。
DEFAULT_PERSISTENT_CACHE_TEXTS = []


def _ensure_model_files():
    missing = [
        path for path in (VOCAB_PATH, LEXICON_PATH, ACOUSTIC_PATH, VOCODER_PATH)
        if not os.path.isfile(path)
    ]
    if missing:
        raise FileNotFoundError("missing TTS model files: " + ", ".join(missing))


def _load_vocab(path):
    m = {}
    with open(path) as f:
        for line in f:
            p = line.strip().split()
            if len(p) >= 2:
                m[p[0]] = int(p[1])
    return m


def _load_lexicon(path):
    m = {}
    with open(path) as f:
        for line in f:
            p = line.strip().split()
            if len(p) >= 2:
                m[p[0]] = p[1:]
    return m


PUNCT_MAP = {
    "，": ",", "。": ".", "：": ",", "；": ",",
    "！": "!", "？": "?", "、": ",", "“": '"', "”": '"',
    "‘": "'", "’": "'", "（": "(", "）": ")",
    ":": ",", ";": ",",
}

SENTENCE_PUNCT = "，。！？；、：,.!?;:"
DROP_PUNCT = set(
    "（）()【】[]{}《》<>“”\"‘’'`·~～@#￥$%^&*_+=|\\/—-"
)

DIGITS = {"0": "零", "1": "一", "2": "二", "3": "三", "4": "四",
           "5": "五", "6": "六", "7": "七", "8": "八", "9": "九"}


def _convert_digits(text: str) -> str:
    result = []
    i = 0
    while i < len(text):
        if text[i].isdigit():
            start = i
            while i < len(text) and text[i].isdigit():
                i += 1
            has_decimal = False
            if i < len(text) and text[i] == '.' and i + 1 < len(text) and text[i + 1].isdigit():
                has_decimal = True
                i += 1
                while i < len(text) and text[i].isdigit():
                    i += 1
            num_str = text[start:i]
            if has_decimal:
                int_part, dec_part = num_str.split('.')
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


def _normalize_tts_text(text: str) -> str:
    """清洗 TTS 文本，同时保留能帮助模型断句的标点。"""
    text = _convert_digits(str(text or ""))
    result = []
    last_space = False
    for ch in text:
        if ch in SENTENCE_PUNCT:
            punct = PUNCT_MAP.get(ch, ch)
            if result and result[-1] not in ",.!?;:":
                result.append(punct)
            last_space = False
            continue
        if ch.isspace() or ch in DROP_PUNCT:
            if result and not last_space:
                result.append(" ")
                last_space = True
            continue
        result.append(ch)
        last_space = False
    return re.sub(r"\s+", " ", "".join(result)).strip()


def _g2p(text, vocab, lexicon):
    tokens = []
    text = _normalize_tts_text(str(text))
    i = 0
    while i < len(text):
        ch = text[i]
        pch = PUNCT_MAP.get(ch, ch)

        if pch in vocab and not ("\u4e00" <= pch <= "\u9fff" or "a" <= pch <= "z" or "A" <= pch <= "Z"):
            tokens.append(vocab[pch])
            i += 1
            continue

        if pch in ("'", '"', ""):
            i += 1
            continue

        matched = False
        for end in range(min(i + 6, len(text)), i, -1):
            word = text[i:end]
            if word in lexicon:
                for py in lexicon[word]:
                    tid = vocab.get(py)
                    if tid is not None:
                        tokens.append(tid)
                matched = True
                i = end
                break
        if matched:
            continue

        if ch in lexicon:
            for py in lexicon[ch]:
                tid = vocab.get(py)
                if tid is not None:
                    tokens.append(tid)
        elif "\u4e00" <= ch <= "\u9fff":
            try:
                py_list = pinyin(ch, style=Style.TONE3)
                if py_list and py_list[0]:
                    tid = vocab.get(py_list[0][0])
                    if tid is not None:
                        tokens.append(tid)
            except Exception:
                pass
        elif "a" <= ch <= "z" or "A" <= ch <= "Z":
            tid = vocab.get(ch)
            if tid is None:
                tid = vocab.get(ch.lower())
            if tid is None:
                tid = vocab.get(ch.upper())
            if tid is not None:
                tokens.append(tid)
        i += 1

    return tokens


def _synth(tokens, acoustic_sess, vocoder_sess):
    x = np.array([tokens], dtype=np.int64)
    x_len = np.array([len(tokens)], dtype=np.int64)
    noise = np.array([0.667], dtype=np.float32)
    lscale = np.array([1.0], dtype=np.float32)

    mel = acoustic_sess.run(None, {"x": x, "x_length": x_len, "noise_scale": noise, "length_scale": lscale})[0]
    out = vocoder_sess.run(None, {"mels": mel.astype(np.float32)})
    mag, cx, cy = out[0], out[1], out[2]
    spec = mag * (cx + 1j * cy)

    n_fft = 1024
    spec_scaled = spec * (2.0 / n_fft)
    _, audio = scisig.istft(spec_scaled[0], nperseg=n_fft, noverlap=n_fft - 256)

    rms = np.sqrt(np.mean(audio ** 2))
    if rms > 1e-6:
        audio = audio * (TARGET_RMS / rms)
    audio = np.clip(audio, -0.99, 0.99).astype(np.float32)

    return audio, 16000


def _postprocess_speech(audio, sr):
    """对抗 Jieli USB 功放静音后的吞音。

    机制（均已实测）：
    1. 流首唤醒：功放冷开机吞掉流里第一声 ~0.2s —— 由 _speak 在整段最前
       垫唤醒音解决，效果确认，首字稳定；
    2. 缝唤醒：内部停顿（逗号、句末分块缝）>=80ms 时，下一词起音前功放
       处于半睡状态，弱起音（「你」的鼻音 n，仅 -43dB 且只有十几毫秒）
       被吃掉，强起音（「大」的塞音瞬间 -13dB）能自己砸醒所以幸存。
       处理：与流首同款——每个缝的开头垫一个唤醒音（220Hz@-30dB，
       被上一字尾音掩蔽，几乎听不见），随后保留 0.25s 静音
       （流首实测唤醒后 300ms 内功放不凉），总缝长 ~0.4s。
    3. 缝后起音前 150ms 加 +12dB 半余弦衰减增益兜底。

    缝检测用两档阈值：高阈值找缝，低阈值收边——缝两端能量在高低阈值
    之间的鼻音起音/句尾余音不算静音，避免把「你」的 n 起音当缝替换掉。
    """
    env = np.abs(audio)
    peak = float(np.max(env)) if env.size else 1.0
    # 高阈值必须很低：鼻音起音和句尾衰减的峰值都能超过 2% 峰值，
    # 会把停顿切成碎段导致漏检。0.2% ≈ -54dB。
    thr_hi = max(peak * 0.002, 1e-4)
    thr_lo = 1e-4  # -80dB：数字本底之上、鼻音起音之下
    is_sil = env < thr_hi
    n = len(audio)
    gaps = []
    i = 0
    while i < n:
        if not is_sil[i]:
            i += 1
            continue
        j = i
        while j < n and is_sil[j]:
            j += 1
        # 收边：从两端剥掉 energy >= thr_lo 的起音/余音段
        si, ei = i, j
        while si < ei and env[si] >= thr_lo:
            si += 1
        while ei > si and env[ei - 1] >= thr_lo:
            ei -= 1
        if ei - si >= int(sr * 0.08) and 0 < si < n and ei < n:
            gaps.append((si, ei))
        i = j

    def _boost(seg, floor_on=True):
        if seg.size == 0:
            return seg
        r = min(int(sr * 0.15), seg.size)
        # 不做 +12dB 整体增益：强起音（塞擦音爆发 ~0.3）被 ×3.98 削顶到
        # 0.99 变成方波咔声（符号后「今/山」起音实测满幅逐样点跳变）。
        # 弱起音有下面垫底兜住，不需要额外增益。
        out = np.clip(seg, -0.99, 0.99).astype(np.float32)
        # 窗式垫底：10ms 窗 RMS 低于 -12dB 的起音窗整体放大到 -12dB。
        # 实测弱起音（「你」的鼻音 n，仅 -46dB）过不了功放的静音唤醒闸，
        # 时好时坏；强起音（「大」的塞音 ~-13dB）从不被吃——把弱起音抬到
        # 略高于塞音的水平即可。按窗归一保波形（逐样本抬底会把元音过零
        # 点拉平失真）。抬起后从起音点做 20ms 半余弦淡入，消除
        # 0→-12dB 的阶跃咔哒。
        if r > 0:
            win = max(int(sr * 0.01), 1)
            # -12dB RMS：比「大」的塞音起音（-13.3dB RMS）再高 1.5dB，
            # 确保弱起音垫底后必然能自己砸开功放的静音闸
            floor_rms = 0.25
            h = out[:r]
            raised_any = False
            # 垫底只用于开头第一段（流首，用户拍板）：中间各段的弱起音保持
            # 自然——功放偶尔吞字可以接受，不给起音加工留咔声的机会。
            if floor_on:
                for s in range(0, len(h), win):
                    segw = h[s:s + win]
                    if segw.size == 0:
                        continue
                    rmsv = float(np.sqrt(np.mean(segw.astype(np.float64) ** 2)))
                    if 1e-6 < rmsv < floor_rms:
                        segw *= (floor_rms / rmsv)
                        raised_any = True
            # 起音窗上限：模型把塞擦音爆发（今 j / 天 t / 山 sh 等）合成到
            # -2dB RMS、峰值近满幅（实测 ±0.97），小喇叭放出来就是偶尔的
            # 「咔/噗」。压到 0.32（与「大」的爆发同量级）——爆发后面的
            # 元音自然比爆发响，听感仍是正常塞音。
            ceil_rms = 0.32
            for s in range(0, len(h), win):
                segw = h[s:s + win]
                if segw.size == 0:
                    continue
                rmsv = float(np.sqrt(np.mean(segw.astype(np.float64) ** 2)))
                if rmsv > ceil_rms:
                    segw *= (ceil_rms / rmsv)
            out[:r] = h
            if raised_any:
                onset = -1
                for s in range(0, min(r, int(sr * 0.25))):
                    if abs(float(out[s])) > 0.05:
                        onset = s
                        break
                if onset >= 0:
                    # 淡入 20ms：5ms 实测起音像一声「咔」（瞬时爬升听感），
                    # 20ms 无咔声投诉。掉字根因是唤醒音干扰，去掉唤醒音后
                    # 20ms 淡入已够，不需要瞬态斜率。
                    fade = min(int(sr * 0.02), r - onset)
                    k = np.arange(fade, dtype=np.float32)
                    out[onset:onset + fade] *= (0.5 * (1.0 - np.cos(np.pi * k / fade))).astype(np.float32)
            # DEBUG 埋点
            try:
                with open("/tmp/pp_debug.log", "a") as _f:
                    _wins = [float(np.sqrt(np.mean(out[s:s + win].astype(np.float64) ** 2))) for s in range(0, min(r, 18 * win), win)]
                    _f.write(f"boost seg_len={seg.size} r={r} first18win_rms={[f'{v:.4f}' for v in _wins]}\n")
            except OSError:
                pass
        return out

    # DEBUG 埋点
    try:
        with open("/tmp/pp_debug.log", "a") as _f:
            _f.write(f"gaps={[(round(si / sr, 3), round(ei / sr, 3)) for si, ei in gaps]} n={n} sr={sr} thr_hi={thr_hi:.5f} thr_lo={thr_lo:.5f} peak={peak:.4f}\n")
    except OSError:
        pass

    if not gaps:
        return _boost(audio)

    # 缝 = 固定 0.25s 纯静音，不用唤醒音：
    # 唤醒音各版本（缝头+0.25s/0.10s 静音、直连起音）实测都仍 ~50% 掉字，
    # 说明 -30dB 的音对功放开闸无效。流首保留垫底起音（用户拍板），
    # 缝后的词起音保持自然——偶尔掉字可接受，不给起音加工留咔声机会。
    gap_sil = np.zeros(int(sr * 0.25), dtype=np.float32)
    out = [_boost(audio[: gaps[0][0]])]
    for idx, (si, ei) in enumerate(gaps):
        out.append(gap_sil)
        seg_end = gaps[idx + 1][0] if idx + 1 < len(gaps) else n
        seg = audio[ei:seg_end]
        # 两缝之间 <150ms 的「小岛」= 模型合成的词尾残段：词的元音尾音被
        # 模型内部的静音坑与主词隔开（实测孤立元音尾峰值 0.8~0.9），播出
        # 来像偶尔一声怪响。直接并入静音——词本身早已被听成完整，残段无感。
        if seg.size < int(sr * 0.15):
            out.append(gap_sil)
        else:
            out.append(_boost(seg, floor_on=False))
    # 段尾 30ms 半余弦收尾：句末分块处模型硬切（尾样点 ±0.5 直落静音，
    # 实测逐样点跳变就是用户听到的「咔」）。给每段（含块间小岛）收一个
    # 自然淡出，尾样点乘到 0，硬切变平滑。
    fade_tail = int(sr * 0.03)
    for idx, seg in enumerate(out):
        if seg.size > fade_tail:
            t = np.arange(fade_tail, dtype=np.float32)
            seg = seg.copy()
            seg[-fade_tail:] *= (0.5 * (1.0 + np.cos(np.pi * t / fade_tail))).astype(np.float32)
            out[idx] = seg
    return np.concatenate(out).astype(np.float32)


def _wake_tone(sr):
    """功放冷启动唤醒音。

    现象：流里第一声会触发 Jieli USB 功放开机，开机头 ~0.2s 的声音被吃掉；
    开过机后 0.4s 静音内保持热态，中间起音都完好。所以整段语音开头垫一个
    轻低频音替真实语音扛下开机，lead 静音期间功放不凉，语音起音即完整。

    实测：±1LSB 数字打点无效（需要真实模拟信号），220Hz@-30dB 有效；
    0.15s 长度用户无感知（隔了 300ms 静音才出声）。
    """
    n = int(sr * 0.15)
    t = np.arange(n, dtype=np.float32) / sr
    return (np.sin(2 * np.pi * 220.0 * t) * 0.031).astype(np.float32)


def _split_text_for_tts(text: str, max_chars: int = MAX_TTS_CHARS):
    text = re.sub(r"\s+", " ", str(text or "").strip())
    if not text:
        return []
    # 只在句末标点断块，逗号/顿号/分号不断：
    # 分块之间只有很短的静音缝，新块是合成器从零起振（起音很弱），
    # 逗号后跟着的音节听着就像被吞掉（“你好，你好”只听到第二个“好”）。
    # 整段合成让模型自己处理逗号停顿，第二个词才有自然的强起音。
    parts = re.split(r"([。！？!?])", text)
    chunks = []
    current = ""
    for idx in range(0, len(parts), 2):
        sentence = parts[idx]
        punct = parts[idx + 1] if idx + 1 < len(parts) else ""
        piece = _normalize_tts_text(sentence + punct)
        if not piece:
            continue
        if len(piece) > max_chars:
            for start in range(0, len(piece), max_chars):
                sub = piece[start:start + max_chars]
                if current:
                    chunks.append(current)
                    current = ""
                chunks.append(sub)
            continue
        if current and len(current) + len(piece) > max_chars:
            chunks.append(current)
            current = piece
        else:
            current += piece
    if current:
        chunks.append(current)
    return chunks


class PythonTtsNode(Node):
    def __init__(self):
        super().__init__("guide_tts_node")
        self.declare_parameter("status_topic", "/guide_tts/status")
        self.declare_parameter("interrupt_topic", "/guide_tts/interrupt")
        self.declare_parameter("speak_service", "/guide_voice/speak")
        self.declare_parameter("audio_device", "")
        self.declare_parameter("player", "aplay")
        # lead 静音吸收 aplay/USB 开机吃样：300ms 实测不够（第一个字仍被吃），
        # 500ms 够；>=0.6s 会让功放进深睡眠，反而吞掉整段起音。
        # 起音本身已由 _postprocess 垫底，不再依赖唤醒音。
        self.declare_parameter("lead_silence_ms", 500)
        self.declare_parameter("tail_silence_ms", 80)
        self.declare_parameter(
            "cache_dir",
            str(Path.home() / ".cache" / "system_manager" / "tts_python"),
        )
        self.declare_parameter(
            "persistent_cache_texts",
            DEFAULT_PERSISTENT_CACHE_TEXTS,
        )
        # 讲解词缓存目录：前端「保存并生成音频」预生成的 wav（键 = sha256(清洗后文本)）。
        # 生成脚本 backend/scripts/tts_generate.py 使用同一目录与同一清洗函数，
        # 生成时已烘焙前后静音与吞字后处理，命中时直接播放。
        self.declare_parameter(
            "guide_cache_dir",
            str(Path.home() / ".cache" / "system_manager" / "tts_python" / "guide"),
        )

        self._cache_dir = Path(
            os.path.expanduser(str(self.get_parameter("cache_dir").value))
        )
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._persistent_cache_dir = self._cache_dir / "persistent"
        self._persistent_cache_dir.mkdir(parents=True, exist_ok=True)
        self._guide_cache_dir = Path(
            os.path.expanduser(str(self.get_parameter("guide_cache_dir").value))
        )
        self._guide_cache_dir.mkdir(parents=True, exist_ok=True)
        self._persistent_cache_texts = {
            _normalize_tts_text(str(text))
            for text in self.get_parameter("persistent_cache_texts").value
            if str(text).strip()
        }
        # Older versions cached every sentence directly under cache_dir.
        # Remove those mixed entries once; persistent entries now live separately.
        for legacy_path in self._cache_dir.glob("*.wav"):
            try:
                legacy_path.unlink()
            except OSError:
                pass
        model_signature = "|".join(
            f"{path}:{os.path.getmtime(path) if os.path.isfile(path) else 0}"
            for path in (ACOUSTIC_PATH, VOCODER_PATH, VOCAB_PATH, LEXICON_PATH)
        )
        self._cache_model_signature = model_signature

        _ensure_model_files()
        self.get_logger().info("Loading vocab & lexicon...")
        self._vocab = _load_vocab(VOCAB_PATH)
        self._lexicon = _load_lexicon(LEXICON_PATH)
        self.get_logger().info(f"Vocab: {len(self._vocab)}, Lexicon: {len(self._lexicon)}")

        self.get_logger().info("Loading ONNX models...")
        opt = ort.SessionOptions()
        opt.intra_op_num_threads = 6
        opt.inter_op_num_threads = 2
        self._acoustic = ort.InferenceSession(ACOUSTIC_PATH, opt)
        self._vocoder = ort.InferenceSession(VOCODER_PATH, opt)
        self.get_logger().info("Models ready")

        status_topic = str(self.get_parameter("status_topic").value)
        interrupt_topic = str(self.get_parameter("interrupt_topic").value)
        self._status_pub = self.create_publisher(String, status_topic, 10)
        # 讲解任务自己的语音服务名（参数可改）：与巡检的 /voice/speak 分开，
        # 两套任务系统互不依赖
        speak_service = str(self.get_parameter("speak_service").value)
        self._speak_srv = self.create_service(Speak, speak_service, self._on_speak)
        self._interrupt_sub = self.create_subscription(String, interrupt_topic, self._on_interrupt, 10)

        self._generation = 0
        self._state_lock = threading.Lock()
        self._queue = queue.Queue(maxsize=QUEUE_MAXSIZE)
        self._player_proc = None
        # 仅在收到"明确要求抢占"的请求时为 True；排队请求不打断当前播放
        self._force_stop = False
        self._closed = False

        self._last_text = ""
        self._last_text_time = 0.0
        # 正在播放的原文。同一句话还在播时，重复请求直接丢弃——
        # 否则 interrupt_current=true 的重复调用会杀掉正在播的自己（吞字）。
        self._playing_text = ""

        self._worker = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker.start()
        self.get_logger().info(
            f"PythonTtsNode ready, persistent_cache_texts={len(self._persistent_cache_texts)}"
        )

    def _on_say(self, msg: String, interrupt: bool = True):
        text = (msg.data or "").strip()
        if not text:
            return

        now = time.time()
        if text == self._last_text and now - self._last_text_time < DEDUP_INTERVAL:
            return
        # 这句话正在播：直接丢新请求（否则抢占式重复调用会杀掉正在播的自己）
        if text == self._playing_text:
            self.get_logger().info(f"Say dropped (already playing): {text[:40]}")
            return
        self._last_text = text
        self._last_text_time = now

        with self._state_lock:
            self._generation += 1
            gen = self._generation

        # 只有明确要求抢占时才打断当前播放并清空队列；
        # 否则仅排队，等上一条自然播完（顺序播报场景不应互相打断）。
        if interrupt:
            self._force_stop = True
            self._interrupt_player()
            try:
                while not self._queue.empty():
                    self._queue.get_nowait()
            except queue.Empty:
                pass

        try:
            self._queue.put_nowait((gen, text))
        except queue.Full:
            pass

    def _on_speak(self, request, response):
        text = (request.text or "").strip()
        if not text:
            response.accepted = False
            response.message = "empty text"
            return response
        self._on_say(String(data=text), interrupt=bool(request.interrupt_current))
        response.accepted = True
        response.message = "queued"
        return response

    def _interrupt_player(self):
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

    def _on_interrupt(self, msg: String):
        reason = (msg.data or "interrupt").strip() or "interrupt"
        self._force_stop = True
        with self._state_lock:
            self._generation += 1
            gen = self._generation
        try:
            while not self._queue.empty():
                self._queue.get_nowait()
        except queue.Empty:
            pass
        self._interrupt_player()
        self._publish_status("interrupted", reason, gen)

    def _publish_status(self, state, text="", gen=0):
        payload = json.dumps(
            {"state": state, "text": text, "generation": gen, "timestamp": int(time.time() * 1000)},
            ensure_ascii=False,
        )
        self._status_pub.publish(String(data=payload))

    def _is_current(self, gen) -> bool:
        with self._state_lock:
            return int(gen) == int(self._generation)

    def _worker_loop(self):
        while not self._closed and rclpy.ok():
            try:
                gen, text = self._queue.get(timeout=0.2)
            except queue.Empty:
                continue
            try:
                self._speak(gen, text)
            except Exception as e:
                self.get_logger().error(f"TTS failed: {e}")
                self._publish_status("error", text, gen)

    def _speak(self, gen, text):
        self.get_logger().info(f"Say: {text[:60]}")
        normalized_text = _normalize_tts_text(text)
        persistent_cache = normalized_text in self._persistent_cache_texts
        cache_key = hashlib.sha256(
            f"{self._cache_model_signature}|{normalized_text}".encode("utf-8")
        ).hexdigest()
        cache_path = self._persistent_cache_dir / f"{cache_key}.wav"
        if persistent_cache and cache_path.is_file() and cache_path.stat().st_size > 44:
            self.get_logger().info(f"TTS cache hit: {cache_path.name}")
            self._play_wav(gen, text, str(cache_path))
            return

        # 讲解词缓存：前端「保存并生成音频」预生成的 wav。键与生成脚本一致
        # （sha256(清洗后文本)，不含模型签名）；文件在生成时已含前后静音与
        # 吞字后处理，直接播放。未命中自动回退实时合成（永不静音）。
        guide_key = hashlib.sha256(normalized_text.encode("utf-8")).hexdigest()
        guide_path = self._guide_cache_dir / f"{guide_key}.wav"
        if guide_path.is_file() and guide_path.stat().st_size > 44:
            self.get_logger().info(f"TTS guide cache hit: {guide_path.name}")
            self._play_wav(gen, text, str(guide_path))
            return

        t0 = time.time()
        segments = []
        sr = 16000
        for chunk in _split_text_for_tts(text):
            if not self._is_current(gen):
                self.get_logger().info("TTS synthesis canceled before playback")
                return
            try:
                tokens = _g2p(chunk, self._vocab, self._lexicon)
                if not tokens:
                    self.get_logger().warn(f"Skip empty TTS tokens: {chunk[:40]}")
                    continue
                audio, sr = _synth(tokens, self._acoustic, self._vocoder)
                if not self._is_current(gen):
                    self.get_logger().info("TTS synthesis canceled after chunk")
                    return
                segments.append(audio)
                # 块间静音：0.12s 太短，下一块起音（合成器从零起振、天然偏弱）
                # 会被功放吃掉。句末分块的场景下 0.25s 听感无明显停顿。
                segments.append(np.zeros(int(sr * 0.25), dtype=np.float32))
            except Exception as exc:
                self.get_logger().warn(f"Skip TTS chunk failed: {chunk[:40]} ({exc})")
        if not segments:
            raise RuntimeError("no valid TTS audio segments")
        audio = np.concatenate(segments)
        # 拉长逗号等内部停顿并给停顿后的起音补增益（功放唤醒吞音）
        audio = _postprocess_speech(audio, sr)
        lead_ms = max(0, int(self.get_parameter("lead_silence_ms").value))
        tail_ms = max(0, int(self.get_parameter("tail_silence_ms").value))
        # 流首不再用唤醒音：220Hz 经小喇叭回放失真成「ci」声，用户反感。
        # 起音已由 _postprocess 垫底到 -12dB（与「大」同级，能自己开闸），
        # lead 静音只需吸收 aplay/USB 开机吃样（实测 0.3s 不够、0.45s 够）。
        pads = []
        if lead_ms > 0:
            pads.append(np.zeros(int(sr * lead_ms / 1000.0), dtype=np.float32))
        pads.append(audio)
        if tail_ms > 0:
            pads.append(np.zeros(int(sr * tail_ms / 1000.0), dtype=np.float32))
        audio = np.concatenate(pads)
        dt = time.time() - t0
        dur = len(audio) / sr
        self.get_logger().info(f"  {dur:.1f}s in {dt:.2f}s (RTF={dt/dur:.3f})")

        temp_dir = str(self._persistent_cache_dir) if persistent_cache else None
        temp_prefix = f".{cache_key}_" if persistent_cache else "tts_"
        fd, wav_path = tempfile.mkstemp(prefix=temp_prefix, suffix=".wav", dir=temp_dir)
        os.close(fd)
        try:
            with wave.open(wav_path, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sr)
                wf.writeframes((audio * 32767).astype(np.int16).tobytes())

            if not self._is_current(gen):
                self.get_logger().info("TTS playback canceled before start")
                return

            if persistent_cache:
                os.replace(wav_path, cache_path)
                wav_path = ""
                self.get_logger().info(f"TTS cache stored: {cache_path.name}")
                self._play_wav(gen, text, str(cache_path))
            else:
                self.get_logger().info("TTS transient audio: delete after playback")
                self._play_wav(gen, text, wav_path)
        finally:
            if wav_path:
                try:
                    os.remove(wav_path)
                except OSError:
                    pass

    def _pad_cached_wav(self, wav_path: str) -> str:
        """给已缓存的 wav 补上前置静音，避免旧缓存仍吞字。"""
        lead_ms = max(0, int(self.get_parameter("lead_silence_ms").value))
        if lead_ms <= 0 or not wav_path:
            return ""
        try:
            with wave.open(wav_path, "rb") as src:
                channels = src.getnchannels()
                sampwidth = src.getsampwidth()
                framerate = src.getframerate()
                frames = src.readframes(src.getnframes())
        except Exception as exc:
            self.get_logger().warn(f"TTS cache pad skipped: {exc}")
            return ""
        n_lead = int(framerate * lead_ms / 1000.0)
        silence = b"\x00" * (n_lead * channels * sampwidth)
        fd, padded_path = tempfile.mkstemp(prefix="tts_lead_", suffix=".wav")
        os.close(fd)
        with wave.open(padded_path, "wb") as dst:
            dst.setnchannels(channels)
            dst.setsampwidth(sampwidth)
            dst.setframerate(framerate)
            dst.writeframes(silence + frames)
        return padded_path

    def _play_wav(self, gen, text, wav_path):
        if not self._is_current(gen):
            self.get_logger().info("TTS playback canceled before start")
            return

        play_path = wav_path
        padded_path = ""
        # 永久缓存是旧文件，合成阶段的前置静音补不上，播放时再垫一次。
        if Path(wav_path).resolve().parent == self._persistent_cache_dir.resolve():
            padded_path = self._pad_cached_wav(wav_path)
            if padded_path:
                play_path = padded_path

        player = str(self.get_parameter("player").value or "aplay").strip() or "aplay"
        audio_device = str(self.get_parameter("audio_device").value or "").strip()
        cmd = [player]
        if os.path.basename(player) == "aplay" and audio_device:
            cmd += ["-D", audio_device]
        cmd.append(play_path)

        # 记录正在播放的原文，供 _on_say 判重（同一句话播放中不再受理）
        self._playing_text = text
        try:
            # stderr 捕获：aplay 断流时会打 "underrun!!!"，用来实锤吞字是否
            # 是 ALSA/USB 流欠载（CPU 抖动）导致，而不是功放静音。
            proc = subprocess.Popen(cmd, start_new_session=True, stderr=subprocess.PIPE)
            with self._state_lock:
                self._player_proc = proc

            self._publish_status("start", text, gen)
            interrupted = False
            while proc.poll() is None:
                # 只有被明确要求抢占时，新请求才会打断当前播放；
                # 仅排队的新请求（generation 已更新但未要求抢占）不打断。
                if self._force_stop and not self._is_current(gen):
                    interrupted = True
                    self._interrupt_player()
                    break
                time.sleep(0.05)
            try:
                return_code = proc.wait(timeout=1.0)
            except subprocess.TimeoutExpired:
                interrupted = True
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except Exception:
                    proc.kill()
                return_code = proc.wait(timeout=1.0)

            with self._state_lock:
                if self._player_proc is proc:
                    self._player_proc = None
                # 当前这条自然播完且没有更新的请求在等，解除抢占标记
                if self._generation == gen:
                    self._force_stop = False

            err_out = ""
            try:
                err_out = (proc.stderr.read() or b"").decode("utf-8", "replace").strip()
            except Exception:
                pass
            if err_out:
                self.get_logger().warn(f"aplay stderr: {err_out[-400:]}")

            if interrupted:
                self._publish_status("interrupted", text, gen)
            elif return_code == 0:
                self._publish_status("end", text, gen)
            else:
                self.get_logger().error(f"TTS player failed: cmd={cmd}, return_code={return_code}")
                self._publish_status("error", text, gen)
        finally:
            self._playing_text = ""
            if padded_path:
                try:
                    os.remove(padded_path)
                except OSError:
                    pass

    def destroy_node(self):
        self._closed = True
        with self._state_lock:
            self._generation += 1
        self._interrupt_player()
        return super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = PythonTtsNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
