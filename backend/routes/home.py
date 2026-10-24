"""主页（工作台）接口"""
from flask import Blueprint
from store import load

from .utils import ok

bp = Blueprint('home', __name__)


@bp.get('/api/home/overview')
def overview():
    """工作台统计概览：地图 / 讲解方案 / 讲解点数量、发布情况、最近更新"""
    maps = load('maps.json')['rows']
    plans = load('plans.json')['rows']
    guides = load('guides.json')['rows']

    def _by_time(row):
        return row.get('updateTime') or row.get('createTime') or ''

    return ok({
        'mapTotal': len(maps),
        'mapPublished': len([m for m in maps if m.get('status') == 1]),
        'planTotal': len(plans),
        'planEnabled': len([p for p in plans if p.get('status') == 1]),
        'guideTotal': len(guides),
        'guideEnabled': len([g for g in guides if g.get('status') == 1]),
        'recentMaps': sorted(maps, key=_by_time, reverse=True)[:5],
        'recentPlans': sorted(plans, key=_by_time, reverse=True)[:5],
        'recentGuides': sorted(guides, key=_by_time, reverse=True)[:5],
    })
