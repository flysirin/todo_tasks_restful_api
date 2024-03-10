import unittest
import json
from datetime import datetime
from pymysql import OperationalError
from pymysql.connections import Connection
from models import db, Tasks
from app import create_app
import configmodule
from config import LOGIN, PASSWORD, DB_LOGIN, DB_PASS, DB_HOST, DB_PORT


class TestDB(unittest.TestCase):
    """Tests DB"""
    auth_credentials = (LOGIN, PASSWORD)
    db_name = 'test_database'

    def test_access_password_login_db(self):

        # test wrong db password
        try:
            with self.assertRaises(OperationalError):
                with Connection(host=DB_HOST, port=int(DB_PORT),
                                user=DB_LOGIN, password='wrong_pass') as con:
                    pass
        except Exception as e:
            self.fail(f"Fail test wrong_pass db: {e}")

        # test wrong db login
        try:
            with self.assertRaises(OperationalError):
                with Connection(host=DB_HOST, port=int(DB_PORT),
                                user='wrong_login', password=DB_PASS) as con:
                    pass
        except Exception as e:
            self.fail(f"Fail test wrong_login db: {e}")

        # test create database
        try:
            with Connection(host=DB_HOST, port=int(DB_PORT),
                            user=DB_LOGIN, password=DB_PASS) as con:
                cur = con.cursor()
                cur.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
                cur.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
                cur.close()

        except Exception as e:
            self.fail(f"Fail test create db: {e}")

        # test write to database
        try:
            with Connection(host=DB_HOST, port=int(DB_PORT),
                            user=DB_LOGIN, password=DB_PASS, database=self.db_name) as con:
                cur = con.cursor()
                cur.execute("""CREATE TABLE todo_tasks(
                                 id INT AUTO_INCREMENT PRIMARY KEY,
                                 title VARCHAR(100),
                                 description TEXT
                                 );""")
                cur.execute("""INSERT INTO todo_tasks VALUES(NULL, 'task_1', 'description_1');""")
                con.commit()

        except Exception as e:
            self.fail(f"Fail test write to db: {e}")

        # test read
        try:
            with Connection(host=DB_HOST, port=int(DB_PORT),
                            user=DB_LOGIN, password=DB_PASS, database=self.db_name) as con:
                cur = con.cursor()
                cur.execute("""SELECT title, description FROM todo_tasks""")
                row = cur.fetchall()[0]
                self.assertEqual(('task_1', 'description_1'), row)

        except Exception as e:
            self.fail(f"Fail test read from db: {e}")

        # drop test database
        try:
            with Connection(host=DB_HOST, port=int(DB_PORT),
                            user=DB_LOGIN, password=DB_PASS) as con:
                cur = con.cursor()
                cur.execute(f"DROP DATABASE IF EXISTS {self.db_name}")

        except Exception as e:
            self.fail(f"Fail drop db: {e}")


class TestErrorDB(unittest.TestCase):
    """Test error handlers DB with App"""

    auth_credentials = (LOGIN, PASSWORD)

    def test_handler_database_not_exist(self):
        app = create_app(configmodule.TestingConfig)
        self.client = app.test_client()
        with Connection(host=DB_HOST, port=int(DB_PORT),
                        user=DB_LOGIN, password=DB_PASS) as con:
            cur = con.cursor()

            db_name = configmodule.TestingConfig.DB_TEST_NAME
            cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
            cur.close()

        result = self.client.get("/todo", auth=self.auth_credentials)

        self.assertEqual(500, result.status_code)
        self.assertEqual({'message': 'Database error'}, json.loads(result.data))

    def test_handler_wrong_login_db(self):
        wrong_login = "wrong_login"

        class WrongLoginConfig(configmodule.TestingConfig):
            SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://' \
                                      f'{wrong_login}:{DB_PASS}@' \
                                      f'{DB_HOST}:{DB_PORT}/test_mysql_db'

        app = create_app(WrongLoginConfig)
        self.client = app.test_client()
        result = self.client.get('/todo', auth=self.auth_credentials)

        self.assertEqual(500, result.status_code)
        self.assertEqual({'message': 'Database error'}, json.loads(result.data))

    def test_handler_wrong_password_db(self):
        wrong_pass = "wrong_login"

        class WrongPasswordConfig(configmodule.TestingConfig):
            SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://' \
                                      f'{DB_LOGIN}:{wrong_pass}@' \
                                      f'{DB_HOST}:{DB_PORT}/test_mysql_db'

        app = create_app(WrongPasswordConfig)
        self.client = app.test_client()
        result = self.client.get('/todo', auth=self.auth_credentials)

        self.assertEqual(500, result.status_code)
        self.assertEqual({'message': 'Database error'}, json.loads(result.data))

    def test_handler_wrong_connection_to_db(self):
        wrong_port = 8888

        class WrongConnectionConfig(configmodule.TestingConfig):
            SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://' \
                                      f'{DB_LOGIN}:{DB_PASS}@' \
                                      f'{DB_HOST}:{wrong_port}/test_mysql_db'

        app = create_app(WrongConnectionConfig)
        self.client = app.test_client()
        result = self.client.get('/todo', auth=self.auth_credentials)

        self.assertEqual(500, result.status_code)
        self.assertEqual({'message': 'Database error'}, json.loads(result.data))


class TestAPI(unittest.TestCase):
    """Tests app with DB"""

    app = create_app(config_module=configmodule.TestingConfig)
    auth_credentials = (LOGIN, PASSWORD)

    def setUp(self):
        """Stuff to do before every test."""

        self.client = self.app.test_client()

        with self.app.app_context(), Connection(host=DB_HOST, port=int(DB_PORT),
                                                user=DB_LOGIN, password=DB_PASS) as con:
            cur = con.cursor()

            db_name = configmodule.TestingConfig.DB_TEST_NAME
            cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            db.drop_all()
            db.create_all()
            db.session.commit()

            task_add = Tasks(title='New task 1.0', description='Create database MySQL')
            db.session.add(task_add)
            db.session.commit()

    def tearDown(self):
        """Stuff to do after every test."""
        with self.app.app_context():
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
        with self.app.app_context():
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

        with self.app.app_context():
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

    def test_handler_data_error(self):
        """Test of an attempt to write a value in the title that is greater than expected"""
        data = json.dumps({
            'title': 'Too much loooooooooooooooooooooooooooooooooooooooooooooooo'
                     'oooooooooooooooooooooooooooooooooooooonnnnnngggggggggg Title',
            'description': 'Checking write and read'})
        result = self.client.post("/todo", data=data, content_type='application/json', auth=self.auth_credentials)

        self.assertEqual(result.status_code, 500)
        self.assertEqual({'message': 'Database error: (1406, "Data too long for column \'title\' at row '
                                     '1")'}, json.loads(result.data))

    if __name__ == '__main__':
        unittest.main()
