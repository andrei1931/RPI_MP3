import os
from flask import Flask, render_template, request, flash
import pygame

# Initialize Pygame mixer
pygame.mixer.init()

# Initialize a global list to store the paths of the MP3 files
mp3_files = []

# Define the path to the 'music' directory within the project
MUSIC_DIR = os.path.join(os.getcwd(), 'music')

# Ensure that the 'music' directory exists; create it if it doesn't
os.makedirs(MUSIC_DIR, exist_ok=True)

# Define functions to play, pause, and skip songs
def play_music():
    pygame.mixer.music.load(mp3_files[-1])  # Load the most recently added file
    pygame.mixer.music.play()

def pause_music():
    pygame.mixer.music.pause()

def resume_music():
    pygame.mixer.music.unpause()

def stop_music():
    pygame.mixer.music.stop()

def skip_music():
    if len(mp3_files) > 1:
        mp3_files.pop(0)  # Remove the oldest file
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
    if file and file.filename.endswith('.mp3'):
        filename = os.path.join(MUSIC_DIR, file.filename)
        file.save(filename)
        mp3_files.append(filename)
        play_music()
        flash('File uploaded and played successfully!')
    else:
        flash('Please upload an MP3 file.')
    return 'File uploaded and played successfully'

@app.route('/lista')
def lista():
    # Get list of MP3 files in the 'music' directory
    mp3_files = [f for f in os.listdir(MUSIC_DIR) if f.endswith('.mp3')]
    return render_template('lista.html', mp3_files=mp3_files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
