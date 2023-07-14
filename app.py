# app.py
import subprocess
import uuid
from flask import Flask, request, jsonify, send_file
import requests
from werkzeug.utils import secure_filename
import os
import ffmpeg
from scipy.spatial import distance


def create_app():
    app = Flask(__name__, static_folder='uploads', static_url_path='/uploads')
    app.config['UPLOAD_FOLDER'] = '/app/uploads/'
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    # Other setup code...
    return app


app = create_app()


@app.route('/', methods=['GET'])
def homepage():
    return "Homepage"


@app.route('/hello', methods=['GET'])
def hello():
    return "Hello"

@app.route('/get_similar', methods=['POST'])
def cosine_similarity():
    data = request.json
    query_vector = data['query_vector']
    vector_text_pairs = data['vectors']

    # Extract embeddings and their corresponding texts
    vectors = [pair['embeddings'] for pair in vector_text_pairs]
    texts = [pair['text'] for pair in vector_text_pairs]

    # Calculate cosine similarity for each vector
    # Return the index of the most similar vector
    most_similar_index = max(range(len(vectors)), key=lambda index: 1 - distance.cosine(query_vector, vectors[index]))

    return jsonify({'most_similar_text': texts[most_similar_index]})
    
from moviepy.editor import VideoFileClip

app = Flask(__name__)

def get_video_duration(url):
    # Send a request to download the video
    response = requests.get(url, stream=True)

    # Save the video file temporarily
    with open("temp.mp4", 'wb') as f:
        f.write(response.content)

    # Load the video file
    clip = VideoFileClip("temp.mp4")

    # Return the duration (in seconds)
    return clip.duration

@app.route('/get_video_length', methods=['POST'])
def get_video_length():
    data = request.get_json()
    video_url = data['url']

    # Check if url is not null
    if not video_url:
        return jsonify({"error": "Missing video URL"}), 400

    try:
        # Get video length
        length = get_video_duration(video_url)
        return jsonify({"length": length})
    except Exception as e:
        return jsonify({"error": "Unable to retrieve video length"}), 500

