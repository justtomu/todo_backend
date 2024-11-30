from flask import request, jsonify
from flask.views import MethodView
from app.extensions import db
from app.models import Task


class TaskListAPI(MethodView):
    def get(self):
        page = request.args.get('page', 1, type=int)
        sort_by = request.args.get('sort_by', 'id')
        sort_order = request.args.get('sort_order', 'asc')

        valid_sort_fields = ['id', 'username', 'email', 'is_completed']
        if sort_by not in valid_sort_fields:
            return jsonify({'error': 'Invalid sort field'}), 400

        order_by = getattr(Task, sort_by)
        if sort_order == 'desc':
            order_by = order_by.desc()

        tasks_query = Task.query.order_by(order_by)
        paginated_tasks = tasks_query.paginate(page=page, per_page=3)

        return jsonify({
            'tasks': [task.to_dict() for task in paginated_tasks.items],
            'total': paginated_tasks.total,
            'page': paginated_tasks.page,
            'pages': paginated_tasks.pages
        })

    def post(self):
        data = request.json
        if not all(key in data for key in ['username', 'email', 'description']):
            return jsonify({'error': 'Missing fields'}), 400

        new_task = Task(
            username=data['username'],
            email=data['email'],
            description=data['description']
        )
        db.session.add(new_task)
        db.session.commit()

        return jsonify(new_task.to_dict()), 201
