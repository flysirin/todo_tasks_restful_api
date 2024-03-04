from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_restful import fields
db = SQLAlchemy()


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)


task_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'completed': fields.Boolean,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    # 'uri': fields.Url('task'),
}
