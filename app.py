from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Get the directory where app.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_dir, 'songs.json')

# Load songs data
with open(json_file_path, 'r') as f:
    SONGS = json.load(f)

@app.route('/health')
def health():
    return jsonify({"status": "OK"})

@app.route('/songs', methods=['GET'])
def get_songs():
    return jsonify(SONGS)

@app.route('/song/<int:id>', methods=['GET'])
def get_song(id):
    song = next((song for song in SONGS if song['id'] == id), None)
    if song:
        return jsonify(song)
    return jsonify({"error": "Song not found"}), 404

@app.route('/song', methods=['POST'])
def create_song():
    new_song = request.get_json()
    if any(song['id'] == new_song['id'] for song in SONGS):
        return jsonify({"error": "Song with this ID already exists"}), 409
    SONGS.append(new_song)
    return jsonify(new_song), 201

@app.route('/song/<int:id>', methods=['PUT'])
def update_song(id):
    song = next((song for song in SONGS if song['id'] == id), None)
    if not song:
        return jsonify({"error": "Song not found"}), 404
    update_data = request.get_json()
    song.update(update_data)
    return jsonify(song)

@app.route('/song/<int:id>', methods=['DELETE'])
def delete_song(id):
    song = next((song for song in SONGS if song['id'] == id), None)
    if not song:
        return jsonify({"error": "Song not found"}), 404
    SONGS.remove(song)
    return '', 204

if __name__ == '__main__':
    app.run(port=5000)
