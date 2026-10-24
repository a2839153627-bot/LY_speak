"""讲解点接口

数据文件：data/guides.json
讲解点字段：
    id          主键
    planId      所属讲解方案 ID（归属关系由方案派生地图）
    mapId       所属地图 ID（由方案的绑定地图自动派生）
    mapName     所属地图名称（冗余存储，便于列表展示）
    planName    所属方案名称（读取时动态注入，不落库）
    pointName   讲解点名称
    x / y       坐标（地图坐标系）
    angle       朝向角度（度）
    stayTime    停留时长（秒）
    content     讲解词（文本）
    status      启用状态：0 停用 / 1 启用
    sort        排序号（同一方案内由小到大执行）
    createTime / updateTime
"""
from flask import Blueprint, request
from store import load, next_id, now_str, save

from .utils import fail, ok, table

bp = Blueprint('guide', __name__)

_DATA = 'guides.json'


def _get_guide(db, guide_id):
    for row in db['rows']:
        if row.get('id') == guide_id:
            return row
    return None


def _plan_info(plan_id):
    """根据方案 ID 取 (planId, mapId, mapName)，方案不存在返回 None"""
    for row in load('plans.json')['rows']:
        if row.get('id') == plan_id:
            return row.get('id'), row.get('mapId'), row.get('mapName', '')
    return None


def _attach_plan_names(rows):
    """为讲解点行动态注入所属方案名称（方案改名后自动保持最新）"""
    if not rows:
        return rows
    names = {p.get('id'): p.get('planName', '') for p in load('plans.json')['rows']}
    for row in rows:
        row['planName'] = names.get(row.get('planId'), '')
    return rows


def _to_number(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


@bp.get('/api/guide/list')
def list_guide():
    """讲解点列表，支持按名称模糊搜索、按所属方案 / 地图过滤"""
    keyword = (request.args.get('pointName') or '').strip()
    plan_id = (request.args.get('planId') or '').strip()
    map_id = (request.args.get('mapId') or '').strip()
    status = (request.args.get('status') or '').strip()

    rows = load(_DATA)['rows']
    if keyword:
        rows = [r for r in rows if keyword in (r.get('pointName') or '')]
    if plan_id != '':
        rows = [r for r in rows if str(r.get('planId')) == plan_id]
    if map_id != '':
        rows = [r for r in rows if str(r.get('mapId')) == map_id]
    if status != '':
        rows = [r for r in rows if str(r.get('status')) == status]

    rows = sorted(rows, key=lambda r: (r.get('mapId', 0), r.get('sort', 0), r.get('id', 0)))
    return table(_attach_plan_names(rows))


@bp.get('/api/guide/<int:guide_id>')
def get_guide(guide_id):
    db = load(_DATA)
    row = _get_guide(db, guide_id)
    if row is None:
        return fail('讲解点不存在', code=404)
    return ok(_attach_plan_names([row])[0])


@bp.get('/api/guide/byMap/<int:map_id>')
def list_guide_by_map(map_id):
    """查询某地图下的全部讲解点（跨方案，供地图页联查）"""
    rows = [r for r in load(_DATA)['rows'] if r.get('mapId') == map_id]
    rows = sorted(rows, key=lambda r: (r.get('planId', 0), r.get('sort', 0), r.get('id', 0)))
    return ok(_attach_plan_names(rows))


@bp.get('/api/guide/byPlan/<int:plan_id>')
def list_guide_by_plan(plan_id):
    """查询某讲解方案下的全部讲解点（供方案配置页联查）"""
    rows = [r for r in load(_DATA)['rows'] if r.get('planId') == plan_id]
    rows = sorted(rows, key=lambda r: (r.get('sort', 0), r.get('id', 0)))
    return ok(rows)


@bp.post('/api/guide')
def add_guide():
    data = request.get_json(silent=True) or {}
    name = (data.get('pointName') or '').strip()
    plan_id = data.get('planId')
    if not name:
        return fail('讲解点名称不能为空')
    if plan_id in (None, ''):
        return fail('请选择所属讲解方案')

    plan = _plan_info(int(plan_id))
    if plan is None:
        return fail('所属讲解方案不存在')

    _, map_id, map_name = plan
    db = load(_DATA)
    row = {
        'id': next_id(db),
        'planId': int(plan_id),
        'mapId': map_id,
        'mapName': map_name,
        'pointName': name,
        'x': _to_number(data.get('x')),
        'y': _to_number(data.get('y')),
        'angle': _to_number(data.get('angle')),
        'stayTime': int(_to_number(data.get('stayTime'), 10)),
        'content': data.get('content', ''),
        'status': int(data.get('status', 1)),
        'sort': int(_to_number(data.get('sort'))),
        'createTime': now_str(),
        'updateTime': now_str(),
    }
    db['rows'].append(row)
    save(_DATA, db)
    return ok(_attach_plan_names([row])[0], '新增成功')


@bp.put('/api/guide')
def update_guide():
    data = request.get_json(silent=True) or {}
    guide_id = data.get('id')
    if guide_id is None:
        return fail('缺少讲解点 ID')

    db = load(_DATA)
    row = _get_guide(db, int(guide_id))
    if row is None:
        return fail('讲解点不存在', code=404)

    for field in ('pointName', 'content'):
        if field in data:
            row[field] = data[field]
    for field in ('x', 'y', 'angle'):
        if field in data:
            row[field] = _to_number(data[field])
    for field in ('stayTime', 'status', 'sort'):
        if field in data:
            row[field] = int(_to_number(data[field]))
    # 变更归属方案时，同步派生地图信息
    if data.get('planId') not in (None, ''):
        plan = _plan_info(int(data['planId']))
        if plan is None:
            return fail('所属讲解方案不存在')
        row['planId'] = plan[0]
        row['mapId'] = plan[1]
        row['mapName'] = plan[2]
    row['updateTime'] = now_str()
    save(_DATA, db)
    return ok(_attach_plan_names([row])[0], '修改成功')


@bp.put('/api/guide/sort')
def sort_guides():
    """按传入的点位 ID 顺序重排某方案下的讲解点，body: { planId, ids: [...] }"""
    data = request.get_json(silent=True) or {}
    plan_id = data.get('planId')
    ids = data.get('ids')
    if plan_id in (None, '') or not isinstance(ids, list):
        return fail('参数不完整')

    db = load(_DATA)
    order = {int(gid): idx for idx, gid in enumerate(ids)}
    changed = False
    for row in db['rows']:
        if row.get('planId') == int(plan_id) and row.get('id') in order:
            row['sort'] = (order[row['id']] + 1) * 10
            row['updateTime'] = now_str()
            changed = True
    if changed:
        save(_DATA, db)
    return ok(msg='排序已保存')


@bp.delete('/api/guide/<int:guide_id>')
def delete_guide(guide_id):
    db = load(_DATA)
    row = _get_guide(db, guide_id)
    if row is None:
        return fail('讲解点不存在', code=404)

    db['rows'] = [r for r in db['rows'] if r.get('id') != guide_id]
    save(_DATA, db)
    return ok(msg='删除成功')
