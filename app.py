from flask import Flask, jsonify, make_response
from flask_restful import Api, Resource, reqparse, marshal_with
from flask_httpauth import HTTPBasicAuth
from models import db, Tasks, task_fields
from config import LOGIN, PASSWORD, DATABASE, HOST, PORT

from datetime import datetime

app = Flask(__name__, static_url_path="")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

api = Api(app)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == LOGIN:
        return PASSWORD
    return None


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)


class TaskListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('description', type=str, default="",
                                   location='json')
        super(TaskListAPI, self).__init__()

    @marshal_with(task_fields)
    def get(self):
        tasks = Tasks.query.order_by(Tasks.id).all()
        return tasks

    @marshal_with(task_fields)
    def post(self):
        args = self.reqparse.parse_args()

        max_id = db.session.query(db.func.max(Tasks.id)).scalar()
        title = args.get('title', '')
        description = args.get('description', '')
        completed = args.get('completed', False)
        created_at = datetime.utcnow().replace(microsecond=0)

        task_add = Tasks(id=max_id + 1, title=title, description=description,
                         completed=completed, created_at=created_at)
        try:
            db.session.add(task_add)
            db.session.commit()

        except BaseException as e:
            db.session.rollback()
            return make_response(jsonify({'message': str(e)}), 500)

        return task_add


class TaskAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('completed', type=bool, location='json')
        self.reqparse.add_argument('created_at', type=str, location='json')
        self.reqparse.add_argument('updated_at', type=str, location='json')
        super(TaskAPI, self).__init__()

    @marshal_with(task_fields)
    def get(self, id):
        task = Tasks.query.filter_by(id=id).first_or_404(description=f'Task with id {id} not found')
        return task

    @marshal_with(task_fields)
    def put(self, id):
        task = Tasks.query.filter_by(id=id).first_or_404(description=f'Task with id {id} not found')
        args = self.reqparse.parse_args()

        try:
            task.title = args.get('title', '')
            task.description = args.get('description', '')
            task.completed = args.get('completed', False)
            task.updated_at = datetime.utcnow().replace(microsecond=0)
            db.session.commit()

        except BaseException as e:
            db.session.rollback()
            return make_response(jsonify({'message': str(e)}), 500)

        return task

    @marshal_with(task_fields)
    def delete(self, id):
        task = Tasks.query.filter_by(id=id).first_or_404(description=f'Task with id {id} not found')
        try:
            db.session.delete(task)
            db.session.commit()
        except BaseException as e:
            db.session.rollback()
            return make_response(jsonify({'message': str(e)}), 500)
        return task


api.add_resource(TaskListAPI, '/todo', endpoint='tasks')
api.add_resource(TaskAPI, '/todo/<int:id>', endpoint='task')

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
