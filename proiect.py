from flask import Flask, render_template, request, flash
import pygame

# Initialize Pygame mixer
pygame.mixer.init()

# Initialize a global list to store the names of the MP3 files
mp3_files = []

# Define functions to play, pause, and skip songs
def play_music():
    pygame.mixer.music.load(mp3_files[i])
    pygame.mixer.music.play()

def pause_music():
    pygame.mixer.music.pause()

def resume_music():
    pygame.mixer.music.unpause()

def stop_music():
    pygame.mixer.music.stop()

def skip_music():
    global i
    i = (i + 1) % len(mp3_files)
    play_music()

app = Flask(__name__)

# Set a secret key for Flask to use for securely generating CSRF tokens
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = file.filename
    file.save(filename)
    global mp3_files
    mp3_files.append(filename)
    play_music()
    flash('File uploaded and played successfully!')
    return 'File uploaded and played successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)