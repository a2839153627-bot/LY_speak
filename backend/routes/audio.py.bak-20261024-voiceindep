"""讲解词音频预生成接口

前端「保存并生成音频」按钮保存完草稿后调用 POST /api/guide/audio/generate，
把该方案（或全部启用方案）的讲解词提前合成为 wav，放到语音节点的讲解词
缓存目录（~/.cache/system_manager/tts_python/guide）。机器人到点播报时语音
节点先查缓存命中直接播放文件，未命中自动回退实时合成（永不静音）。

生成/清理都通过子进程调 backend/scripts/tts_generate.py：纯文件操作，
不创建 ROS 节点、不播放、不出声，对正在使用机器人的其他人零干扰。
生成任务在 daemon 线程里跑，状态存进程内 dict（加锁），前端轮询查询。
"""
import json
import os
import subprocess
import threading
import time

from flask import Blueprint, request

from store import BASE_DIR, load, now_str

from .utils import fail, ok

bp = Blueprint('audio', __name__)

_SCRIPT = os.path.join(BASE_DIR, 'scripts', 'tts_generate.py')

# 生成任务状态（进程内内存态：Flask 重启后丢失，重新点按钮即可，接口幂等）
_jobs = {}
_jobs_lock = threading.Lock()
_last_job_id = None


def _enabled_plan_ids():
    """全部启用方案（status==1）的 ID 列表"""
    return [p['id'] for p in load('plans.json')['rows'] if p.get('status') == 1]


def _collect_texts(plan_ids):
    """收集方案集合下启用点位（status==1）的非空讲解词"""
    rows = load('guides.json')['rows']
    texts = []
    for r in rows:
        if r.get('planId') not in plan_ids:
            continue
        if r.get('status') != 1:
            continue
        content = str(r.get('content') or '').strip()
        if content:
            texts.append(content)
    return texts


def _run_script(mode, texts, generate):
    """子进程跑生成脚本：先 source humble 与 LY_speak_ws（讲解任务自己的
    voice 包进 PYTHONPATH），从 stdin 传 JSON，读 stdout 的一行 JSON 结果。

    mode: 'generate' 合成 generate 子集中缺失的 wav；'cleanup' 只清理。
    texts: 全量启用讲解词（清理白名单，防止误删其他方案的 wav）。
    """
    payload = json.dumps(
        {'texts': texts, 'generate': generate}, ensure_ascii=False
    )
    bash_cmd = (
        'source /opt/ros/humble/setup.bash && '
        'source /home/smart/LY_speak_ws/ros2/install/setup.bash && '
        f'python3 {_SCRIPT} {mode}'
    )
    env = dict(os.environ, ROS_DOMAIN_ID='6', PYTHONUNBUFFERED='1')
    try:
        proc = subprocess.run(
            ['bash', '-lc', bash_cmd],
            input=payload.encode('utf-8'),
            capture_output=True,
            env=env,
            timeout=1800,
        )
    except subprocess.TimeoutExpired:
        return None, '生成超时（30 分钟）'
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or b'').decode('utf-8', errors='replace')
        return None, f'生成脚本退出码 {proc.returncode}: {err[-800:]}'
    try:
        result = json.loads((proc.stdout or b'{}').decode('utf-8', errors='replace'))
    except json.JSONDecodeError:
        return None, '生成脚本输出不是合法 JSON'
    return result, None


@bp.post('/api/guide/audio/generate')
def generate_audio():
    """启动讲解词音频预生成任务。body: { planId? }（缺省 = 全部启用方案）"""
    data = request.get_json(silent=True) or {}
    plan_id = data.get('planId')

    all_plan_ids = _enabled_plan_ids()
    if plan_id in (None, ''):
        gen_texts = _collect_texts(all_plan_ids)
    else:
        gen_texts = _collect_texts([int(plan_id)])
    if not gen_texts:
        return fail('没有可生成的讲解词（启用方案下无启用点位或讲解词为空）')

    global _last_job_id
    with _jobs_lock:
        if any(j.get('state') == 'running' for j in _jobs.values()):
            return fail('已有音频生成任务进行中', code=409)
        job_id = int(time.time() * 1000)
        _last_job_id = job_id
        _jobs[job_id] = {
            'jobId': job_id,
            'state': 'running',
            'total': len(gen_texts),
            'generated': 0,
            'cacheHits': 0,
            'cleaned': 0,
            'message': '正在生成讲解词音频…',
            'startedAt': now_str(),
            'finishedAt': '',
        }
        # 只保留最近 20 个历史任务
        for k in list(_jobs.keys()):
            if k != job_id and len(_jobs) > 20:
                _jobs.pop(k, None)

    def _worker():
        all_texts = _collect_texts(all_plan_ids)
        result, err = _run_script('generate', all_texts, gen_texts)
        with _jobs_lock:
            job = _jobs[job_id]
            if err:
                job.update({'state': 'error', 'message': err})
            else:
                cleaned = len(result.get('cleaned') or [])
                errors = result.get('errors') or []
                job.update({
                    'state': 'error' if errors and not result.get('generated') else 'done',
                    'generated': result.get('generated', 0),
                    'cacheHits': result.get('cache_hits', 0),
                    'cleaned': cleaned,
                    'message': (
                        f"生成 {result.get('generated', 0)} 个 / 已存在 {result.get('cache_hits', 0)} 个"
                        f" / 清理过期 {cleaned} 个"
                        + (f"；{len(errors)} 条失败（到点将实时合成兜底）" if errors else '')
                    ),
                })
            job['finishedAt'] = now_str()

    threading.Thread(target=_worker, daemon=True).start()
    return ok({'jobId': job_id, 'state': 'running', 'total': len(gen_texts)}, '生成任务已启动')


@bp.get('/api/guide/audio/status')
def audio_status():
    """查询生成任务状态。params: { jobId? }（缺省 = 最新任务；无任务返回 state=idle）"""
    job_id = (request.args.get('jobId') or '').strip()
    with _jobs_lock:
        if job_id:
            job = _jobs.get(int(job_id))
        else:
            job = _jobs.get(_last_job_id) if _last_job_id else None
    return ok(dict(job) if job else {'state': 'idle'})


@bp.post('/api/guide/audio/cleanup')
def audio_cleanup():
    """手动清理过期音频：删除缓存目录里不在全量启用讲解词集合中的 wav"""
    all_texts = _collect_texts(_enabled_plan_ids())
    result, err = _run_script('cleanup', all_texts, all_texts)
    if err:
        return fail(err)
    cleaned = result.get('cleaned') or []
    return ok({'removed': cleaned, 'count': len(cleaned)}, f'已清理 {len(cleaned)} 个过期音频文件')
