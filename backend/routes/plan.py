"""讲解方案管理接口

数据文件：data/plans.json
讲解方案字段：
    id          主键
    planName    方案名称
    mapId       绑定的地图 ID（创建后不可更改）
    mapName     绑定地图名称（冗余存储，便于列表展示）
    status      启用状态：0 停用 / 1 启用
    remark      备注
    createTime / updateTime

关联关系：地图 1 ── n 讲解方案 1 ── n 讲解点（guides.json 通过 planId 归属）
"""
from flask import Blueprint, request
from store import load, next_id, now_str, save

from .utils import fail, ok, table

bp = Blueprint('plan', __name__)

_DATA = 'plans.json'
_GUIDES = 'guides.json'


def _get_plan(db, plan_id):
    for row in db['rows']:
        if row.get('id') == plan_id:
            return row
    return None


def _map_row(map_id):
    """根据地图 ID 取地图行"""
    for row in load('maps.json')['rows']:
        if row.get('id') == map_id:
            return row
    return None


def _point_count(plan_id):
    """统计方案下的讲解点数量"""
    return len([g for g in load(_GUIDES)['rows'] if g.get('planId') == plan_id])


@bp.get('/api/plan/list')
def list_plan():
    """方案列表，支持按名称模糊搜索、按所属地图 / 状态过滤"""
    keyword = (request.args.get('planName') or '').strip()
    map_id = (request.args.get('mapId') or '').strip()
    status = (request.args.get('status') or '').strip()

    rows = load(_DATA)['rows']
    if keyword:
        rows = [r for r in rows if keyword in (r.get('planName') or '')]
    if map_id != '':
        rows = [r for r in rows if str(r.get('mapId')) == map_id]
    if status != '':
        rows = [r for r in rows if str(r.get('status')) == status]

    rows = sorted(rows, key=lambda r: r.get('id', 0), reverse=True)
    # 附带讲解点数量
    for row in rows:
        row['pointCount'] = _point_count(row.get('id'))
    return table(rows)


@bp.get('/api/plan/byMap/<int:map_id>')
def list_plan_by_map(map_id):
    """查询某地图下的全部方案（供地图页选择归属方案 / 联查）"""
    rows = [r for r in load(_DATA)['rows'] if r.get('mapId') == map_id]
    rows = sorted(rows, key=lambda r: r.get('id', 0))
    for row in rows:
        row['pointCount'] = _point_count(row.get('id'))
    return ok(rows)


@bp.get('/api/plan/<int:plan_id>')
def get_plan(plan_id):
    db = load(_DATA)
    row = _get_plan(db, plan_id)
    if row is None:
        return fail('讲解方案不存在', code=404)
    row['pointCount'] = _point_count(plan_id)
    return ok(row)


@bp.post('/api/plan')
def add_plan():
    data = request.get_json(silent=True) or {}
    name = (data.get('planName') or '').strip()
    map_id = data.get('mapId')
    if not name:
        return fail('方案名称不能为空')
    if map_id in (None, ''):
        return fail('请选择绑定地图')

    map_row = _map_row(int(map_id))
    if map_row is None:
        return fail('绑定的地图不存在')

    db = load(_DATA)
    # 同一地图下方案名称不允许重复
    if any(r.get('mapId') == int(map_id) and r.get('planName') == name for r in db['rows']):
        return fail('该地图下已存在同名方案')

    row = {
        'id': next_id(db),
        'planName': name,
        'mapId': int(map_id),
        'mapName': map_row.get('mapName', ''),
        'status': int(data.get('status', 1)),
        'remark': data.get('remark', ''),
        'createTime': now_str(),
        'updateTime': now_str(),
    }
    db['rows'].append(row)
    save(_DATA, db)
    return ok(row, '新增成功')


@bp.put('/api/plan')
def update_plan():
    """修改方案：名称 / 状态 / 备注（绑定地图创建后不可更改）"""
    data = request.get_json(silent=True) or {}
    plan_id = data.get('id')
    if plan_id is None:
        return fail('缺少方案 ID')

    db = load(_DATA)
    row = _get_plan(db, int(plan_id))
    if row is None:
        return fail('讲解方案不存在', code=404)

    if 'planName' in data:
        name = (data.get('planName') or '').strip()
        if not name:
            return fail('方案名称不能为空')
        if any(
            r.get('mapId') == row.get('mapId') and r.get('planName') == name and r.get('id') != row.get('id')
            for r in db['rows']
        ):
            return fail('该地图下已存在同名方案')
        row['planName'] = name
    if 'status' in data:
        row['status'] = int(data['status'])
    if 'remark' in data:
        row['remark'] = data['remark']
    row['updateTime'] = now_str()
    save(_DATA, db)
    return ok(row, '修改成功')


@bp.delete('/api/plan/<int:plan_id>')
def delete_plan(plan_id):
    db = load(_DATA)
    row = _get_plan(db, plan_id)
    if row is None:
        return fail('讲解方案不存在', code=404)

    db['rows'] = [r for r in db['rows'] if r.get('id') != plan_id]
    save(_DATA, db)

    # 联动删除该方案下的讲解点
    gdb = load(_GUIDES)
    gdb['rows'] = [g for g in gdb['rows'] if g.get('planId') != plan_id]
    save(_GUIDES, gdb)
    return ok(msg='删除成功')


def ensure_default_plans():
    """为尚无方案归属的历史讲解点自动创建默认方案（幂等，服务启动时调用）

    规则：按 mapId 分组，将无 planId 的讲解点挂到该地图下 id 最小的方案；
    该地图没有方案时，自动创建一个「{地图名} 讲解方案」。
    """
    gdb = load(_GUIDES)
    orphans = [g for g in gdb['rows'] if g.get('planId') in (None, '')]
    if not orphans:
        return

    maps = {m.get('id'): m for m in load('maps.json')['rows']}
    pdb = load(_DATA)
    plans_by_map = {}
    for p in pdb['rows']:
        plans_by_map.setdefault(p.get('mapId'), []).append(p)

    pdb_changed = False
    for guide in orphans:
        map_id = guide.get('mapId')
        if map_id is None:
            continue  # 无归属地图的历史数据保持原样

        plans = plans_by_map.get(map_id)
        if plans:
            plan = sorted(plans, key=lambda p: p.get('id', 0))[0]
        else:
            map_name = (maps.get(map_id) or {}).get('mapName') or '未命名地图'
            base = f'{map_name} 讲解方案'
            existing = {p.get('planName') for p in pdb['rows']}
            name = base
            seq = 2
            while name in existing:
                name = f'{base}{seq}'
                seq += 1
            plan = {
                'id': next_id(pdb),
                'planName': name,
                'mapId': map_id,
                'mapName': (maps.get(map_id) or {}).get('mapName', ''),
                'status': 1,
                'remark': '系统自动创建，用于收纳历史讲解点',
                'createTime': now_str(),
                'updateTime': now_str(),
            }
            pdb['rows'].append(plan)
            plans_by_map[map_id] = [plan]
            pdb_changed = True
        guide['planId'] = plan['id']

    if pdb_changed:
        save(_DATA, pdb)
    save(_GUIDES, gdb)
