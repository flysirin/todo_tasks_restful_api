import unittest
from app import app, TaskAPI, TaskListAPI
from models import db, Tasks, task_fields     #connect_to_db
import requests
import json
from config import LOGIN, PASSWORD, DATABASE, HOST, PORT


class TestAPI(unittest.TestCase):
    """Tests with DB."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        with app.app_context():
            db.create_all()

            task_add = Tasks(id=1, title='New task 1.0', description='Create database SQLite')
            db.session.add(task_add)
            db.session.commit()

    def tearDown(self):
        """Stuff to do after every test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_todo(self):
        """Test retrieving todo item from db"""

        auth_credentials = (LOGIN, PASSWORD)
        result = self.client.get("/todo/1", auth=auth_credentials)
        self.assertEqual(result.status_code, 200)
        #
        data = json.loads(result.data)
        self.assertEqual(data['title'], "Buy groceries")
        self.assertEqual(data["description"], "Buy eggs and spinach")

    # def test_post_todo(self):
    #     """Test posting a todo item"""
    #
    #     result = self.client.post("/todo/",
    #                               data=json.dumps({
    #                                 "name": "Clean apartment",
    #                                 "description": "Sweep, do dishes"
    #                               }),
    #                               content_type='application/json')
    #
    #     self.assertEqual(result.status_code, 200)
    #
    #     # Check for the item in the db
    #     todo = Todo.query.get(2)
    #     self.assertEqual(todo.name, "Clean apartment")
    #     self.assertEqual(todo.description, "Sweep, do dishes")


if __name__ == '__main__':
    unittest.main()
