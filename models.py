from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class UploadedFile(db.Model):
    __tablename__ = 'uploaded_files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filesize = db.Column(db.String(50))
    filedate = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('files', lazy=True))
