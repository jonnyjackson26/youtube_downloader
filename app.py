from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__, static_folder="dist", static_url_path="")
CORS(app)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route("/download", methods=["POST"])
def download_video():
    data = request.json
    url = data.get("url", "")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Path to the cookies file
        cookies_file = "cookies.txt"  # Replace with your cookies file path

        # Set yt-dlp options, including the cookies file
        ydl_opts = {
            "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
            "format": "best",
            "cookiefile": cookies_file,  # Pass cookies to yt-dlp
        }

        # Download video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = f"{info['title']}.mp4"
            file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

        # Ensure the file exists
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found on server"}), 500

        # Serve the file directly to the client
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        # Log the error for debugging
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Serve React frontend
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# Serve downloads
@app.route("/downloads/<filename>")
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
