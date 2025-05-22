import os
import re
import subprocess
import time
import traceback
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import requests

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

ANIMATION_DIR = "animations"
OUTPUT_FILENAME = "output.mp4"
MEDIA_DIR = "media"
VIDEO_PATH = os.path.join(MEDIA_DIR, "videos", "generated_scene", "1080p15", OUTPUT_FILENAME)

@app.route('/')
def home():
    return "Server is running!"

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior Python developer specialized in Manim (Community Edition v0.18 or later).\n"
                        "Your task is to generate a complete and correct Python script that creates a Manim animation.\n\n"
                        "STRICT INSTRUCTIONS:\n"
                        "- Output must be ONLY valid Python code.\n"
                        "- Do NOT include any extra text like 'Here is the code' or explanations.\n"
                        "- Always start the code with:\n"
                        "    from manim import *\n"
                        "- Always define exactly one scene class:\n"
                        "    class GeneratedScene(Scene):\n"
                        "- Use only standard Manim methods (like Create, FadeIn, Transform, MoveToTarget, wait(), etc.).\n"
                        "- Ensure the code runs with this command:\n"
                        "    manim -pql animations/generated_scene.py GeneratedScene -o output.mp4\n"
                        "- Avoid any deprecated or unstable syntax.\n"
                        "- Do NOT use markdown (```) or comments.\n\n"
                        "USER PROMPT:\n"
                        "\"\"\"\n"
                        "<USER_ANIMATION_REQUEST_HERE>\n"
                        "\"\"\"\n\n"
                        "Output only the clean, correct Python code compatible with ManimCE. No surrounding text."
                    )
                },
                { "role": "user", "content": prompt }
            ]
        )

        code_raw = response.choices[0].message.content.strip()
        code = re.sub(r"^```(?:python)?|```$", "", code_raw, flags=re.MULTILINE).strip()
        code = code.encode('ascii', 'ignore').decode()

        if "from manim" not in code:
            code = "from manim import *\nimport numpy as np\n\n" + code

        os.makedirs(ANIMATION_DIR, exist_ok=True)
        scene_file = os.path.join(ANIMATION_DIR, "generated_scene.py")
        with open(scene_file, "w") as f:
            f.write(code)

        match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\):', code)
        if not match:
            return jsonify({"error": "No Scene class found in code"}), 400
        scene_name = match.group(1)

        subprocess.run([
            "manim", "-ql", scene_file, scene_name,
            "-o", OUTPUT_FILENAME, "-r", "1920,1080",
            "--media_dir", MEDIA_DIR
        ], check=True)

        # Wait until video is fully written
        while not os.path.exists(VIDEO_PATH):
            time.sleep(0.1)

        while True:
            try:
                with open(VIDEO_PATH, "rb") as f:
                    f.read()
                break
            except Exception:
                time.sleep(0.1)

        return send_file(VIDEO_PATH, mimetype="video/mp4")

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Manim rendering failed: {e}"}), 500
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
