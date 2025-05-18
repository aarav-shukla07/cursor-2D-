from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
from llm_interface import get_animation_script
from video_generator import generate_video
import uuid
import requests

app = Flask(__name__)

def get_manim_code_from_openrouter(prompt, model="mistralai/mixtral-8x7b-instruct"):
    api_key = "c8408a93b0b050fb6cf5f46dd7dcb2272865df86af78ebe7f8d0ba418aca9313"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost",  # Required by OpenRouter
        "Content-Type": "application/json",
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert in writing animations using Manim in Python."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print("Error:", response.text)
        return None

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.json.get('prompt')

    manim_code = get_manim_code_from_openrouter(prompt)
    if not manim_code:
        return jsonify({"error": "Failed to get response from OpenRouter"}), 500

    filename = f"scene_{uuid.uuid4().hex}.py"
    filepath = os.path.join("scenes", filename)
    os.makedirs("scenes", exist_ok=True)
    with open(file_path, "w") as f:
        f.write(manim_code)
    
    try:
        command = f"manim -pql {filepath} FormationOfCube -o output.mp4"
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Manim rendering failed", "details": str(e)}), 500

    return send_file("media/videos/scene/output.mp4", mimetype='video/mp4')

@app.route('/download/<resolution>/<filename>', methods=['GET'])
def download(resolution, filename):
    folder_path = f'media/videos/{resolution}'
    return send_from_directory(folder_path, filename, as_attachement=True)

if __name__ == '__main__':
    app.run(debug=True)