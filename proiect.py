from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__,static_url_path='')
app.config['UPLOAD_FOLDER'] = 'music'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Music {self.title}>'

@app.route('/')
def index():
    music_files = Music.query.all()
    return render_template('index.html', music_files=music_files)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        title = request.form['title']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.mp3'):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            new_file = Music(filename=filename, title=title)
            db.session.add(new_file)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/music/<filename>')
def music(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<int:id>')
def delete(id):
    file_to_delete = Music.query.get_or_404(id)
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_to_delete.filename))
        db.session.delete(file_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        flash('Could not delete file')
        return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
