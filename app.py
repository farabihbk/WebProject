from flask import Flask, render_template_string, send_from_directory, url_for
import os

app = Flask(__name__)

VIDEO_FOLDER = os.path.join(os.path.dirname(__file__), 'backend')
ALLOWED_EXTENSIONS = {'mp4', 'webm', 'ogg', 'mov', 'avi', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    videos = [f for f in os.listdir(VIDEO_FOLDER) if allowed_file(f)]
    return render_template_string('''
    <!doctype html>
    <title>Video Sharing App</title>
    <h1>Video Sharing App</h1>
    <ul>
      {% for video in videos %}
        <li>
          <a href="{{ url_for('play_video', filename=video) }}">{{ video }}</a>
        </li>
      {% endfor %}
    </ul>
    ''', videos=videos)

@app.route('/video/<filename>')
def play_video(filename):
    if not allowed_file(filename):
        return "File type not allowed", 403
    return render_template_string('''
    <!doctype html>
    <title>Playing {{ filename }}</title>
    <h1>Playing: {{ filename }}</h1>
    <video width="720" controls autoplay>
      <source src="{{ url_for('get_video', filename=filename) }}" type="video/mp4">
      Your browser does not support the video tag.
    </video>
    <br>
    <a href="{{ url_for('index') }}">Back to list</a>
    ''', filename=filename)

@app.route('/backend/<filename>')
def get_video(filename):
    if not allowed_file(filename):
        return "File type not allowed", 403
    return send_from_directory(VIDEO_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)