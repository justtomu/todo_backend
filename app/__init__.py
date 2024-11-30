from flask import Flask
from app.config import Config
from app.extensions import db, migrate, cors, jwt
from app.views.tasks import TaskListAPI
from app.views.admin import AdminTaskAPI, AdminLoginAPI


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    jwt.init_app(app)

    task_view = TaskListAPI.as_view('tasks')
    app.add_url_rule('/tasks/', view_func=task_view, methods=['GET', 'POST'])

    admin_task_view = AdminTaskAPI.as_view('admin_task')
    app.add_url_rule('/manage/<int:task_id>', view_func=admin_task_view, methods=['PUT'])

    admin_login_view = AdminLoginAPI.as_view('admin_login')
    app.add_url_rule('/admin/login', view_func=admin_login_view, methods=['POST'])

    return app
