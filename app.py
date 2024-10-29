from flask import Flask, request, jsonify
import os
from core import step2_whisper

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
        file.save(file_path)  # Open the file in binary mode
        file_path = step2_whisper.transcribe_audio_to_srt(file_path)
        print("file_path=",file_path)
        if not file_path:
            return jsonify({"error": "Failed to transcribe the audio file"}), 200
        if not os.path.exists(file_path):
            return jsonify({"error": "Failed to transcribe the audio file"}), 200
        print("host url=" , request.host_url)
        # Generate a URL for the client to download the file
        download_url = request.host_url + 'download/' + os.path.basename(file_path)
        print("download_url=",download_url)
        return jsonify({"message": "File successfully uploaded",  "download_url": download_url}), 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)