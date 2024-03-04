import unittest
from app import app
from models import db, Tasks
import json
from config import LOGIN, PASSWORD
from datetime import datetime


class TestAPI(unittest.TestCase):
    """Tests with DB."""

    auth_credentials = (LOGIN, PASSWORD)

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_ECHO'] = True

        with app.app_context():
            db.drop_all()
            db.create_all()

            task_add = Tasks(title='New task 1.0', description='Create database MySQL')
            db.session.add(task_add)
            db.session.commit()

    def tearDown(self):
        """Stuff to do after every test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_task(self):
        """Test retrieving task item from db"""

        result = self.client.get("/todo/1", auth=self.auth_credentials)

        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['title'], 'New task 1.0')
        self.assertEqual(data['description'], 'Create database MySQL')
        self.assertEqual(data['completed'], False)

        try:
            created_at_datetime = datetime.strptime(data['created_at'], '%a, %d %b %Y %H:%M:%S %z')
        except ValueError:
            self.fail(f"Failed to parse 'created_at' value '{data['created_at']}' as a valid datetime")

        self.assertIsInstance(created_at_datetime, datetime)

    def test_post_task(self):
        """Test posting a task item"""

        result = self.client.post("/todo",
                                  data=json.dumps({
                                      'title': 'Database setup',
                                      'description': 'Checking write and read',
                                  }),
                                  content_type='application/json', auth=self.auth_credentials)

        self.assertEqual(result.status_code, 200)

        # Check for the item in the db by id
        with app.app_context():
            task = Tasks.query.filter_by(id=2).first_or_404(description=f'Task with id {id} not found')
        self.assertIsNotNone(task, "Task with ID=2 not found in the database")
        self.assertEqual(task.title, 'Database setup')
        self.assertEqual(task.description, 'Checking write and read')
        self.assertEqual(task.completed, False)

    def test_put_task(self):
        """Test updating a task item"""

        result = self.client.post("/todo",
                                  data=json.dumps({
                                      'title': 'Database setup',
                                      'description': 'Checking write, read',
                                  }),
                                  content_type='application/json', auth=self.auth_credentials)
        self.assertEqual(result.status_code, 200)

        # update task with id=2
        result = self.client.put("/todo/2",
                                 data=json.dumps({
                                     'title': 'Database setup',
                                     'description': 'Checking write, read, update',
                                     'completed': True
                                 }),
                                 content_type='application/json', auth=self.auth_credentials)
        self.assertEqual(result.status_code, 200)

        data = json.loads(result.data)
        self.assertEqual(data['title'], 'Database setup')
        self.assertEqual(data['description'], 'Checking write, read, update')
        self.assertEqual(data['completed'], True)

        try:
            created_at_datetime = datetime.strptime(data['updated_at'], '%a, %d %b %Y %H:%M:%S %z')
        except ValueError:
            self.fail(f"Failed to parse 'created_at' value '{data['created_at']}' as a valid datetime")

        self.assertIsInstance(created_at_datetime, datetime)

    def test_get_tasks(self):
        """Test retrieving tasks items from db"""
        tasks = [
            {
                'title': 'Database setup',
                'description': 'Checking write, read, update',
                'completed': False
            },
            {
                'title': 'Database continue setup',
                'description': 'Test retrieving tasks items from db',
                'completed': False
            }
        ]

        for task in tasks:
            result = self.client.post("/todo",
                                      data=json.dumps({
                                          'title': task['title'],
                                          'description': task['description'],
                                      }),
                                      content_type='application/json', auth=self.auth_credentials)
            self.assertEqual(result.status_code, 200)

        tasks_get_tests = [
            {
                'id': 1,
                'title': 'New task 1.0',
                'description': 'Create database SQLite',
                'completed': False
            },
            {
                'id': 2,
                'title': 'Database setup',
                'description': 'Checking write, read, update',
                'completed': False
            },
            {
                'id': 3,
                'title': 'Database continue setup',
                'description': 'Test retrieving tasks items from db',
                'completed': False
            }
        ]

        with app.app_context():
            result = self.client.get('/todo', auth=self.auth_credentials)
            data = json.loads(result.data)
            self.assertEqual(result.status_code, 200)

            for i, task in enumerate(tasks_get_tests):
                self.assertEqual(task['id'], data[i]['id'])
                self.assertEqual(task['title'], data[i]['title'])
                self.assertEqual(task['completed'], data[i]['completed'])

    def test_delete_tasks(self):
        """Task deletion test items from db and authorized access"""

        result = self.client.post("/todo",
                                  data=json.dumps({
                                      'title': 'Database continue setup',
                                      'description': 'Test retrieving tasks items from db',
                                  }), content_type='application/json', auth=self.auth_credentials)
        self.assertEqual(result.status_code, 200)

        # test Unauthorized access
        result = self.client.delete('/todo/2')
        self.assertEqual(result.json, {'message': 'Unauthorized access'})
        self.assertEqual(result.status_code, 403)

        # test for removing a non-existent element
        result = self.client.delete('/todo/3', auth=self.auth_credentials)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.json, {'message': 'Task with id 3 not found'})

        # test for removing a existent element
        result = self.client.delete('/todo/2', auth=self.auth_credentials)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['title'], 'Database continue setup')
        self.assertEqual(data['description'], 'Test retrieving tasks items from db')

        # test empty db
        self.client.delete('/todo/1', auth=self.auth_credentials)
        result = self.client.get('/todo', auth=self.auth_credentials)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json, [])


if __name__ == '__main__':
    unittest.main()
