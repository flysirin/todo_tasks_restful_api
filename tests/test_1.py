import unittest
from pymysql import OperationalError
from pymysql.connections import Connection
from app import app
from models import db, Tasks
import json
from config import LOGIN, PASSWORD, DB_LOGIN, DB_PASS, DB_HOST, DB_PORT
from datetime import datetime
from error_handlers import register_error_handlers

DB_NAME = 'test_db'


class TestDB:
    """Tests DB"""
    auth_credentials = (LOGIN, PASSWORD)
    register_error_handlers(app)

    def test_access_password_login_db(self):
        try:
            with Connection(host=DB_HOST,
                            port=int(DB_PORT),
                            user=DB_LOGIN,
                            password='wrong_pass') as con:
                pass

        except OperationalError as e:
            # test wrong db password
            self.assertEqual("""(1045, "Access denied for user 'root'@'localhost' (using password: YES)")""",
                             str(e.args))
        try:
            with Connection(host=DB_HOST,
                            port=int(DB_PORT),
                            user='wrong_login',
                            password=DB_PASS) as con:
                pass

        except OperationalError as e:
            # test wrong db login
            self.assertEqual("""(1045, "Access denied for user 'wrong_login'@'localhost' (using password: YES)")""",
                             str(e.args))

        # access test with correct login and password
        try:
            with Connection(host=DB_HOST,
                            port=int(DB_PORT),
                            user=DB_LOGIN,
                            password=DB_PASS) as con:
                cur = con.cursor()
                cur.execute("SHOW DATABASES")

                for databases in cur:
                    print(databases)
                cur.close()
        except OperationalError as e:
            self.assertFalse(e)
            print(e)

    def test_error_handlers(self):

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_ECHO'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_LOGIN}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        data = json.dumps({
            'title': 'Database setupDatabase setup',
            'description': 'Checking write and read'})
        result = self.client.post("/todo", data=data, content_type='application/json', auth=self.auth_credentials)
        print(result.data)
        self.assertEqual(result.status_code, 500)


