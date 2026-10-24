"""JSON 文件存储层

所有业务数据以 JSON 文件形式保存在 backend/data 目录下，统一结构：

    {
        "nextId": 1,          # 自增主键
        "rows": [ {...}, ]    # 数据行
    }

写入时使用线程锁 + 临时文件原子替换，避免并发写坏文件。
"""
import json
import os
import threading
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')

_lock = threading.RLock()

# 各业务数据文件（不存在时自动创建空结构）
_DEFAULT_FILES = ('maps.json', 'plans.json', 'guides.json')


def _file_path(name):
    return os.path.join(DATA_DIR, name)


def _read_raw(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _write_raw(path, data):
    """先写临时文件再原子替换，防止写一半进程退出损坏数据"""
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def ensure_data_files():
    """确保数据目录、上传目录与数据文件存在"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    for name in _DEFAULT_FILES:
        path = _file_path(name)
        if not os.path.exists(path):
            _write_raw(path, {'nextId': 1, 'rows': []})


def load(name):
    """读取数据文件，返回 {'nextId': n, 'rows': [...]}"""
    with _lock:
        ensure_data_files()
        return _read_raw(_file_path(name))


def save(name, data):
    """整体写回数据文件"""
    with _lock:
        ensure_data_files()
        _write_raw(_file_path(name), data)


def next_id(data):
    """从数据集合中取一个自增 ID（调用方负责随后 save）"""
    _id = int(data.get('nextId', 1))
    data['nextId'] = _id + 1
    return _id


def now_str():
    """当前时间字符串，如 2026-10-08 17:41:00"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
