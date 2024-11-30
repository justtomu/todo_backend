from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.extensions import db
from app.models import Task, Admin


class AdminTaskAPI(MethodView):
    @jwt_required()
    def put(self, task_id):
        current_admin = get_jwt_identity()
        if not current_admin:
            return jsonify({'error': 'Unauthorized'}),

        data = request.json
        task = Task.query.get_or_404(task_id)

        if 'description' in data:
            task.description = data['description']
        if 'is_completed' in data:
            task.is_completed = data['is_completed']

        db.session.commit()
        return jsonify(task.to_dict())


class AdminLoginAPI(MethodView):
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            token = create_access_token(identity=admin.username)
            return jsonify({'access_token': token, 'username': username}), 200

        return jsonify({'error': 'Invalid credentials'}), 401
