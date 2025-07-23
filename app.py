import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
from werkzeug.utils import secure_filename
from models import db, User, UploadedFile
from config import Config

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config.from_object(Config)
db.init_app(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')  # Adjust if using different login route
    
    user = User.query.get(session['user_id'])
    files = UploadedFile.query.filter_by(user_id=user.id).all()

    return render_template('index.html', user=user, files=files)

@app.route('/upload', methods=['POST'])
def upload():
    if 'user_id' not in session:
        return redirect('/login')
    
    files = request.files.getlist('files[]')
    user = User.query.get(session['user_id'])

    uploaded = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            size_mb = round(os.path.getsize(filepath) / (1024 * 1024), 1)
            new_file = UploadedFile(
                filename=filename,
                filesize=f"{size_mb} MB",
                filedate=datetime.now().strftime('%Y-%m-%d'),
                user_id=user.id
            )
            db.session.add(new_file)
            uploaded.append(filename)

    db.session.commit()
    return jsonify({'success': True, 'uploaded': uploaded})

@app.route('/delete/<int:file_id>', methods=['POST'])
def delete_file(file_id):
    file = UploadedFile.query.get(file_id)
    if file and file.user_id == session['user_id']:
        db.session.delete(file)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 403

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Dummy login just for demonstration
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return "User not found", 404
    return '''<form method="post">Username: <input name="username"><input type="submit"></form>'''

# DB Init Route
@app.cli.command('init-db')
def init_db():
    db.create_all()
    print("Database initialized!")

if __name__ == '__main__':
    app.run(debug=True)
