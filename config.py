import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}
