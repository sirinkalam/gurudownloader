from flask import Flask, request, send_file, jsonify, render_template
import yt_dlp
import os
import uuid

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template("index.html")   # <-- important


@app.route('/download', methods=['POST'])
def download_video():
    try:
        url = request.form.get('url')
        unique_id = str(uuid.uuid4())

        ydl_opts = {
            "outtmpl": f"{DOWNLOAD_FOLDER}/{unique_id}.%(ext)s",
            "format": "bestvideo+bestaudio/best",
            "quiet": True,
            "noplaylist": True,
            "merge_output_format": "mp4",
            "http_headers": {
            "User-Agent": "Mozilla/5.0"
            },
   
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
