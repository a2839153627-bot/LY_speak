"""接口统一响应工具

响应格式与若依（RuoYi）保持一致，方便前端直接复用：
    单条数据： { code: 200, msg: '操作成功', data: {...} }
    列表数据： { code: 200, msg: '查询成功', rows: [...], total: n }
    失败：     { code: 500, msg: '错误信息' }
"""
from flask import jsonify


def ok(data=None, msg='操作成功'):
    return jsonify(code=200, msg=msg, data=data)


def table(rows, total=None):
    return jsonify(code=200, msg='查询成功', rows=rows, total=total if total is not None else len(rows))


def fail(msg='操作失败', code=500):
    return jsonify(code=code, msg=msg)
