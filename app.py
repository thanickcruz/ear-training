from flask import Flask, render_template, send_from_directory, redirect, url_for, request, session
import random
import os

app = Flask(__name__)
app.secret_key = ""  # Required for session management

# Path to the audio samples
SAMPLES_DIR = os.path.join(app.static_folder, 'samples')

# List of available audio files in the samples directory
sample_files = [f for f in os.listdir(SAMPLES_DIR) if f.endswith('.wav')]

# Initialize session variables if not set
def initialize_session():
    if 'correct_answers' not in session:
        session['correct_answers'] = 0
    if 'total_samples' not in session:
        session['total_samples'] = 0

@app.route('/')
def index():
    initialize_session()  # Ensure session variables are set
    sample = random.choice(sample_files)
    return render_template('index.html', sample=sample, result=None, result_color=None, score=None)

@app.route('/static/samples/<filename>')
def serve_sample(filename):
    return send_from_directory(SAMPLES_DIR, filename)

@app.route('/guess', methods=['POST'])
def guess():
    initialize_session()  # Ensure session variables are set

    # Enharmonic equivalents
    enharmonic_map = {
        "A#": "Bb", "Bb": "A#",
        "C#": "Db", "Db": "C#",
        "D#": "Eb", "Eb": "D#",
        "F#": "Gb", "Gb": "F#",
        "G#": "Ab", "Ab": "G#",
        "A#m": "Bbm", "Bbm": "A#m",
        "C#m": "Dbm", "Dbm": "C#m",
        "D#m": "Ebm", "Ebm": "D#m",
        "F#m": "Gbm", "Gbm": "F#m",
        "G#m": "Abm", "Abm": "G#m"
    }

    user_guess = request.form.get('user_guess').strip()
    sample = request.form.get('sample')
    chord = sample.split('_')[0]

    # Update session variables
    session['total_samples'] += 1

    if user_guess == chord or enharmonic_map.get(user_guess) == chord:
        session['correct_answers'] += 1
        result = "Correct!"
        result_color = "green"
    else:
        result = f"Incorrect! The correct chord was {chord}"
        result_color = "red"

    # Calculate the score
    score = f"{session['correct_answers']} / {session['total_samples']}"

    return render_template('index.html', sample=sample, result=result, result_color=result_color, score=score)

@app.route('/next')
def next_sample():
    initialize_session()  # Ensure session variables are set
    sample = random.choice(sample_files)
    return render_template('index.html', sample=sample, result=None, result_color=None, score=f"{session['correct_answers']} / {session['total_samples']}")

if __name__ == '__main__':
    app.run(debug=True)
