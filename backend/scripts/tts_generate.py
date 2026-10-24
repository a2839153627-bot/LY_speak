#!/usr/bin/env python3
"""讲解词音频预生成脚本（纯文件操作：不创建 ROS 节点、不播放、不出声）。

由后端 routes/audio.py 通过子进程调用（先 source humble 与 LY_speak_ws，
讲解任务自己的 voice 包才会出现在 PYTHONPATH 上）。复用 voice 包
tts_python_node 的文本
清洗 / 分块 / 合成 / 后处理函数，保证生成出来的 wav 与语音节点"实时合成"
路径完全同规格：

  - 缓存键一致：sha256(清洗后的讲解词)，两边都用 _normalize_tts_text；
  - 内容一致：分块合成 + 块间 0.25s 静音 + _postprocess_speech（吞字修复）
    + 前置 500ms / 后置 80ms 静音（与节点参数默认值一致，语音节点播放
    guide 缓存时不会再补静音）。

用法：
  python3 tts_generate.py generate
      # 从 stdin 读 JSON：{"texts": [全量启用讲解词], "generate": [本次要合成的子集]}
      # 合成 generate 子集中缺失的 wav，再按 texts 全集清理孤儿 wav
  python3 tts_generate.py cleanup
      # 从 stdin 读 JSON：{"texts": [...]}，只按该集合清理孤儿 wav（不加载模型）

输出：一行 JSON 结果到 stdout（stderr 可能有模型库的警告，属正常）。
"""
import hashlib
import json
import os
import sys
import wave
from pathlib import Path

import numpy as np
import onnxruntime as ort

from voice.nodes.tts_python_node import (
    ACOUSTIC_PATH,
    LEXICON_PATH,
    VOCAB_PATH,
    VOCODER_PATH,
    _ensure_model_files,
    _g2p,
    _load_lexicon,
    _load_vocab,
    _normalize_tts_text,
    _postprocess_speech,
    _split_text_for_tts,
    _synth,
)

# 与语音节点参数默认值保持一致（tts_python_node.py 里 declare_parameter）：
# lead/tail 静音在生成时直接烘焙进 wav，guide 缓存播放时不再补。
LEAD_SILENCE_MS = 500
TAIL_SILENCE_MS = 80
GUIDE_CACHE_DIR = Path.home() / ".cache" / "system_manager" / "tts_python" / "guide"


def _hash_name(normalized_text: str) -> str:
    """缓存文件名：sha256(清洗后文本)。必须与语音节点 guide 缓存查询一致。"""
    return hashlib.sha256(normalized_text.encode("utf-8")).hexdigest() + ".wav"


def _load_models():
    """加载 ONNX 模型（与语音节点相同的会话配置）"""
    _ensure_model_files()
    vocab = _load_vocab(VOCAB_PATH)
    lexicon = _load_lexicon(LEXICON_PATH)
    opt = ort.SessionOptions()
    opt.intra_op_num_threads = 6
    opt.inter_op_num_threads = 2
    acoustic = ort.InferenceSession(ACOUSTIC_PATH, opt)
    vocoder = ort.InferenceSession(VOCODER_PATH, opt)
    return vocab, lexicon, acoustic, vocoder


def _synthesize(text, vocab, lexicon, acoustic, vocoder):
    """复刻语音节点 _speak 的拼装流程：分块合成 → 块间静音 → 后处理 → 前后静音"""
    segments = []
    sr = 16000
    for chunk in _split_text_for_tts(text):
        tokens = _g2p(chunk, vocab, lexicon)
        if not tokens:
            continue
        audio, sr = _synth(tokens, acoustic, vocoder)
        segments.append(audio)
        # 块间静音与语音节点一致（0.25s），避免下一块弱起音被功放吃掉
        segments.append(np.zeros(int(sr * 0.25), dtype=np.float32))
    if not segments:
        return None
    audio = np.concatenate(segments)
    # 吞字修复后处理（缝替换 / 段尾淡出），与实时合成路径一致
    audio = _postprocess_speech(audio, sr)
    pads = []
    if LEAD_SILENCE_MS > 0:
        pads.append(np.zeros(int(sr * LEAD_SILENCE_MS / 1000.0), dtype=np.float32))
    pads.append(audio)
    if TAIL_SILENCE_MS > 0:
        pads.append(np.zeros(int(sr * TAIL_SILENCE_MS / 1000.0), dtype=np.float32))
    return np.concatenate(pads).astype(np.float32)


def _write_wav(path, audio, sr):
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes((np.clip(audio, -0.99, 0.99) * 32767).astype(np.int16).tobytes())


def _cleanup_orphans(valid_names, result):
    """删除 guide 缓存目录里不在当前全量讲解词集合中的 wav"""
    for f in sorted(GUIDE_CACHE_DIR.glob("*.wav")):
        if f.name in valid_names:
            continue
        try:
            f.unlink()
            result["cleaned"].append(f.name)
        except OSError as exc:
            result["errors"].append({"file": f.name, "error": str(exc)})


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "generate"
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError) as exc:
        print(json.dumps({"mode": mode, "errors": [{"error": f"stdin JSON 解析失败: {exc}"}]}, ensure_ascii=False))
        return 1

    raw_texts = [str(t) for t in (payload.get("texts") or [])]
    gen_texts = [str(t) for t in (payload.get("generate") or raw_texts)]

    # 清洗 + 按清洗后文本去重，跳过空文本
    norm_map = {}
    for t in raw_texts:
        n = _normalize_tts_text(t)
        if n and n not in norm_map:
            norm_map[n] = t
    gen_norms = []
    for t in gen_texts:
        n = _normalize_tts_text(t)
        if n and n not in gen_norms:
            gen_norms.append(n)

    GUIDE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    valid_names = {_hash_name(n) for n in norm_map}

    result = {
        "mode": mode,
        "total": len(gen_norms),
        "generated": 0,
        "cache_hits": 0,
        "cleaned": [],
        "skipped_empty": len(raw_texts) - len(norm_map),
        "errors": [],
    }

    if mode == "generate" and gen_norms:
        vocab, lexicon, acoustic, vocoder = _load_models()
        for n in gen_norms:
            path = GUIDE_CACHE_DIR / _hash_name(n)
            if path.is_file() and path.stat().st_size > 44:
                result["cache_hits"] += 1
                continue
            try:
                audio = _synthesize(norm_map[n], vocab, lexicon, acoustic, vocoder)
                if audio is None:
                    result["skipped_empty"] += 1
                    continue
                tmp = GUIDE_CACHE_DIR / (path.name + ".tmp")
                _write_wav(tmp, audio, 16000)
                os.replace(tmp, path)
                result["generated"] += 1
            except Exception as exc:
                result["errors"].append({"text": norm_map[n][:40], "error": str(exc)})

    _cleanup_orphans(valid_names, result)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
