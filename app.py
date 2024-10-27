from flask import Flask, request, jsonify
import os
from st_components.imports_and_utils import *

app = Flask(__name__)
UPLOAD_FOLDER = 'output/audio/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#add get server status
@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "Server is running"}), 200

@app.route('/upload', methods=['POST'])
def audio_to_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        step2_whisper.transcribe_audio_to_srt(file_path)
        return jsonify({"message": "File successfully uploaded", "file_path": file_path}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)