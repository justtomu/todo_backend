import unittest
from app import create_app
from app.extensions import db
from app.models import Task, Admin


class ToDoAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_task(self):
        response = self.client.post('/tasks/', json={
            'username': 'John Doe',
            'email': 'john@example.com',
            'description': 'Test Task'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Test Task', response.get_json()['description'])

    def test_get_tasks(self):
        with self.app.app_context():
            task1 = Task(username='Alice', email='alice@example.com', description='Task 1')
            task2 = Task(username='Bob', email='bob@example.com', description='Task 2')
            db.session.add_all([task1, task2])
            db.session.commit()

        response = self.client.get('/tasks/?page=1&sort_by=username&sort_order=asc')
        self.assertEqual(response.status_code, 200)
        tasks = response.get_json()['tasks']
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]['username'], 'Alice')

    def test_admin_login(self):
        with self.app.app_context():
            admin = Admin(username="test_admin")
            admin.set_password("password")
            db.session.add(admin)
            db.session.commit()

        response = self.client.post('/admin/login', json={
            'username': 'test_admin',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_json())

    def test_edit_task_as_admin(self):
        with self.app.app_context():
            admin = Admin(username="admin")
            admin.set_password("password")
            db.session.add(admin)

            task = Task(username="User", email="user@example.com", description="Old Task")
            db.session.add(task)
            db.session.commit()

            task_id = task.id

        login_response = self.client.post('/admin/login', json={
            'username': 'admin',
            'password': 'password'
        })
        token = login_response.get_json()['access_token']

        response = self.client.put(f'/manage/{task_id}', headers={
            'Authorization': f'Bearer {token}'
        }, json={
            'description': 'New Description',
            'is_completed': True
        })

        self.assertEqual(response.status_code, 200)
        updated_task = response.get_json()
        self.assertEqual(updated_task['description'], 'New Description')
        self.assertTrue(updated_task['is_completed'])


if __name__ == '__main__':
    unittest.main()
