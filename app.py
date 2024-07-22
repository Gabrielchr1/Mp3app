from flask import Flask, request, jsonify, send_file, render_template
import yt_dlp
import os
from flask_cors import CORS

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL não fornecida.'}), 400

    # Define o nome do arquivo
    output_path = "downloads/audio.mp3"  # Caminho padrão para salvar o arquivo

    # Verifica se a pasta de downloads existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'noplaylist': True,
        # Remover postprocessors para não usar ffmpeg
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
