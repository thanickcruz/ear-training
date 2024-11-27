from flask import Flask, render_template, send_from_directory, redirect, url_for, request
import random
import os

app = Flask(__name__)

# Path to the audio samples
SAMPLES_DIR = os.path.join(app.static_folder, 'samples')

# List of available audio files in the samples directory
sample_files = [f for f in os.listdir(SAMPLES_DIR) if f.endswith('.wav')]

@app.route('/')
def index():
    # Pick a random sample file
    sample = random.choice(sample_files)
    # Extract the chord from the filename (e.g., 'G#m_3.wav' -> 'G#m')
    chord = sample.split('_')[0]
    return render_template('index.html', sample=sample, chord=chord)

@app.route('/static/samples/<filename>')
def serve_sample(filename):
    return send_from_directory(SAMPLES_DIR, filename)

@app.route('/guess', methods=['GET'])
def guess():
    user_guess = request.args.get('user_guess').strip()
    sample = request.args.get('sample')
    chord = sample.split('_')[0]

    if user_guess == chord:
        result = "Correct!"
        result_color = "green"
    else:
        result = f"Incorrect! The correct chord was {chord}"
        result_color = "red"

    # After displaying the result, redirect to the index to load a new sample
    return render_template('index.html', result=result, result_color=result_color, sample=random.choice(sample_files))

if __name__ == '__main__':
    app.run(debug=True)
