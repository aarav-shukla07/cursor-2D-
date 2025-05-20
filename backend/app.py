from flask import Flask, request, jsonify, send_file, send_from_directory
import subprocess
import os
from llm_interface import get_animation_script
from video_generator import generate_video
import uuid
import requests
from flask_cors import CORS
import re
from dotenv import load_dotenv


load_dotenv()



app = Flask(__name__)
CORS(app)



def get_manim_code_from_openrouter(prompt):
    api_key = os.getenv("OPENROUTER_API_KEY")
    print("API Key:", api_key)  # Debugging line to check if the API key is loaded correctly

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set in environment variables")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "openai/gpt-4",  # or whatever model you use on OpenRouter
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)

    if response.status_code != 200:
        raise Exception("OpenRouter API call failed")

    return response.json()['choices'][0]['message']['content']



@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.json.get('prompt')

    manim_code = get_manim_code_from_openrouter(prompt)
    if not manim_code:
        return jsonify({"error": "Failed to get response from OpenRouter"}), 500

    filename = f"scene_{uuid.uuid4().hex}.py"
    filepath = os.path.join("animations", filename)
    os.makedirs("animations", exist_ok=True)
    with open(filepath, "w") as f:
        f.write(manim_code)
    
    try:
        command = f"manim -pql {filepath} FormationOfCube -o output.mp4"
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Manim rendering failed", "details": str(e)}), 500

    return send_file("media/videos/animations/output.mp4", mimetype='video/mp4')

@app.route('/download/<resolution>/<filename>', methods=['GET'])
def download(resolution, filename):
    folder_path = f'media/videos/{resolution}'
    return send_from_directory(folder_path, filename, as_attachement=True)

if __name__ == '__main__':
    app.run(debug=True)