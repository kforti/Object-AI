from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    cognito_username = db.Column(db.String(150), primary_key=True, unique=True)


class Workspace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150), unique=True)
    bucket_name = db.Column(db.String(150), unique=True)
    labelbox_aws_account = db.Column(db.String(100))
    labelbox_external_id = db.Column(db.String(100))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}