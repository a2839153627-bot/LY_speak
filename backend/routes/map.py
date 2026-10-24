"""地图管理接口

数据文件：data/maps.json
地图字段：
    id          主键
    mapName     地图名称
    robotName   所属机器人
    mapFile     地图文件（PGM/YAML/压缩包）在 uploads 下的相对路径
    pointCount  讲解点数量（由讲解点数据自动统计）
    status      发布状态：0 未发布 / 1 已发布
    remark      备注
    chargeX / chargeY / chargeAngle  充电点位（世界坐标米 / 度，与讲解点同坐标系；未设置时为 None）
    keepoutZones                    禁区多边形列表 [[{x, y}, ...], ...]（世界坐标米，与讲解点同坐标系）
    createTime / updateTime
"""
import os
import time

from flask import Blueprint, request
from store import UPLOAD_DIR, load, next_id, now_str, save

from .utils import fail, ok, table

bp = Blueprint('map', __name__)

_DATA = 'maps.json'


def _get_map(db, map_id):
    for row in db['rows']:
        if row.get('id') == map_id:
            return row
    return None


def _related_counts(map_id):
    """统计地图下的讲解方案数 / 讲解点数"""
    plans = load('plans.json')['rows']
    guides = load('guides.json')['rows']
    return (
        len([p for p in plans if p.get('mapId') == map_id]),
        len([g for g in guides if g.get('mapId') == map_id]),
    )


@bp.get('/api/map/list')
def list_map():
    """地图列表，支持按名称模糊搜索、按发布状态过滤"""
    keyword = (request.args.get('mapName') or '').strip()
    status = (request.args.get('status') or '').strip()

    rows = load(_DATA)['rows']
    if keyword:
        rows = [r for r in rows if keyword in (r.get('mapName') or '')]
    if status != '':
        rows = [r for r in rows if str(r.get('status')) == status]

    rows = sorted(rows, key=lambda r: r.get('id', 0), reverse=True)
    # 附带讲解方案 / 讲解点数量
    for row in rows:
        row['planCount'], row['pointCount'] = _related_counts(row.get('id'))
    return table(rows)


@bp.get('/api/map/<int:map_id>')
def get_map(map_id):
    db = load(_DATA)
    row = _get_map(db, map_id)
    if row is None:
        return fail('地图不存在', code=404)
    row['planCount'], row['pointCount'] = _related_counts(map_id)
    return ok(row)


@bp.post('/api/map')
def add_map():
    data = request.get_json(silent=True) or {}
    name = (data.get('mapName') or '').strip()
    if not name:
        return fail('地图名称不能为空')

    db = load(_DATA)
    if any(r.get('mapName') == name for r in db['rows']):
        return fail('地图名称已存在')

    row = {
        'id': next_id(db),
        'mapName': name,
        'robotName': data.get('robotName', ''),
        'mapFile': data.get('mapFile', ''),
        'pgmFile': data.get('pgmFile', ''),
        'yamlFile': data.get('yamlFile', ''),
        'pointCount': 0,
        'status': 0,
        'remark': data.get('remark', ''),
        'chargeX': data.get('chargeX'),
        'chargeY': data.get('chargeY'),
        'chargeAngle': data.get('chargeAngle'),
        'keepoutZones': data.get('keepoutZones') or [],
        'createTime': now_str(),
        'updateTime': now_str(),
    }
    db['rows'].append(row)
    save(_DATA, db)
    return ok(row, '新增成功')


@bp.put('/api/map')
def update_map():
    data = request.get_json(silent=True) or {}
    map_id = data.get('id')
    if map_id is None:
        return fail('缺少地图 ID')

    db = load(_DATA)
    row = _get_map(db, int(map_id))
    if row is None:
        return fail('地图不存在', code=404)

    for field in ('mapName', 'robotName', 'mapFile', 'pgmFile', 'yamlFile', 'remark',
                  'chargeX', 'chargeY', 'chargeAngle', 'keepoutZones'):
        if field in data:
            row[field] = data[field]
    row['updateTime'] = now_str()
    save(_DATA, db)
    return ok(row, '修改成功')


@bp.delete('/api/map/<int:map_id>')
def delete_map(map_id):
    db = load(_DATA)
    row = _get_map(db, map_id)
    if row is None:
        return fail('地图不存在', code=404)

    db['rows'] = [r for r in db['rows'] if r.get('id') != map_id]
    save(_DATA, db)

    # 联动删除该地图下的讲解方案
    pdb = load('plans.json')
    pdb['rows'] = [p for p in pdb['rows'] if p.get('mapId') != map_id]
    save('plans.json', pdb)

    # 联动删除该地图下的讲解点
    gdb = load('guides.json')
    gdb['rows'] = [g for g in gdb['rows'] if g.get('mapId') != map_id]
    save('guides.json', gdb)
    return ok(msg='删除成功')


@bp.post('/api/map/<int:map_id>/publish')
def publish_map(map_id):
    """发布 / 取消发布，body: { status: 1|0 }"""
    data = request.get_json(silent=True) or {}
    status = int(data.get('status', 1))

    db = load(_DATA)
    row = _get_map(db, map_id)
    if row is None:
        return fail('地图不存在', code=404)

    row['status'] = status
    row['updateTime'] = now_str()
    save(_DATA, db)
    return ok(row, '发布成功' if status == 1 else '已取消发布')


@bp.post('/api/map/upload')
def upload_map_file():
    """上传地图文件（PGM/YAML/ZIP 等），保存到 uploads/maps/ 目录"""
    file = request.files.get('file')
    if file is None or not file.filename:
        return fail('未选择文件')

    sub_dir = os.path.join(UPLOAD_DIR, 'maps')
    os.makedirs(sub_dir, exist_ok=True)
    safe_name = os.path.basename(file.filename)
    file_name = f'{int(time.time())}_{safe_name}'
    file.save(os.path.join(sub_dir, file_name))

    return ok({
        'fileName': safe_name,
        'path': f'maps/{file_name}',
        'url': f'/uploads/maps/{file_name}',
    }, '上传成功')


@bp.post('/api/map/upload/files')
def upload_map_files():
    """上传成对的 PGM + YAML 地图文件（新增 / 编辑地图弹窗使用）

    两个文件均为可选，但至少上传一个；
    同一秒上传时通过时间戳前缀 + 原名保证不冲突。
    """
    pgm = request.files.get('pgmFile')
    yaml_file = request.files.get('yamlFile')
    has_pgm = pgm is not None and pgm.filename
    has_yaml = yaml_file is not None and yaml_file.filename
    if not has_pgm and not has_yaml:
        return fail('未选择文件')

    if has_pgm and not pgm.filename.lower().endswith('.pgm'):
        return fail('PGM 文件格式不正确（需为 .pgm）')
    if has_yaml and not yaml_file.filename.lower().endswith(('.yaml', '.yml')):
        return fail('YAML 文件格式不正确（需为 .yaml / .yml）')

    sub_dir = os.path.join(UPLOAD_DIR, 'maps')
    os.makedirs(sub_dir, exist_ok=True)
    stamp = int(time.time())
    result = {}

    if has_pgm:
        name = os.path.basename(pgm.filename)
        saved = f'{stamp}_{name}'
        pgm.save(os.path.join(sub_dir, saved))
        result['pgmName'] = name
        result['pgmFile'] = f'maps/{saved}'
    if has_yaml:
        name = os.path.basename(yaml_file.filename)
        saved = f'{stamp}_{name}'
        yaml_file.save(os.path.join(sub_dir, saved))
        result['yamlName'] = name
        result['yamlFile'] = f'maps/{saved}'

    return ok(result, '上传成功')
