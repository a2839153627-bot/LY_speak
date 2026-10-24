"""LY_Guide 导览讲解机器人 - 后端服务入口

技术栈：Flask + JSON 文件存储
启动：python app.py   （默认监听 0.0.0.0:5000）
"""
import os

from flask import Flask, jsonify, request, send_from_directory

from routes import register_blueprints
from routes.plan import ensure_default_plans
from store import BASE_DIR, UPLOAD_DIR, ensure_data_files

# 前端构建产物目录（部署时由 deploy.py 放到项目根目录的 web/ 下）
WEB_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'web'))


def create_app():
    # static_folder=None：禁用 Flask 内置的 /static 路由，
    # 避免拦截前端构建产物中的 static/ 目录（由 serve_web 统一托管）
    app = Flask(__name__, static_folder=None)
    # 上传文件大小限制 200MB（地图文件可能较大）
    app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

    # 允许跨域（前端 vite 开发代理已处理，直连调试时也能用）
    @app.after_request
    def add_cors_headers(resp):
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        # 前端发版后 index.html 内容会变（引用的 JS 分块文件名带 hash）。
        # 不让浏览器缓存它：否则缓存了旧 index.html 会一直加载旧页面，
        # 看起来就像"前端没生效"。带 hash 的 JS/CSS 分块仍可正常缓存。
        if request.path == '/' or request.path.endswith('index.html'):
            resp.headers['Cache-Control'] = 'no-store'
        return resp

    @app.route('/uploads/<path:filename>')
    def serve_upload(filename):
        """访问上传的地图等静态资源"""
        return send_from_directory(UPLOAD_DIR, filename)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_web(path):
        """托管前端构建产物（web/ 目录），支持 history 路由回退到 index.html"""
        if path.startswith(('api/', 'uploads/')) or not os.path.isdir(WEB_DIR):
            return jsonify(code=404, msg='资源不存在'), 404
        full_path = os.path.join(WEB_DIR, path)
        if path and os.path.isfile(full_path):
            return send_from_directory(WEB_DIR, path)
        return send_from_directory(WEB_DIR, 'index.html')

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify(code=404, msg='接口不存在'), 404

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify(code=500, msg='服务器内部错误'), 500

    ensure_data_files()
    # 历史数据迁移：为无方案归属的讲解点自动创建默认方案（幂等）
    with app.app_context():
        ensure_default_plans()
    register_blueprints(app)
    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
