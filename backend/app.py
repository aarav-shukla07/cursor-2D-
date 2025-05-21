import os
import re
import subprocess
import traceback
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import requests

load_dotenv()

# OpenRouter setup
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

app = Flask(__name__)
CORS(app)

# ANIMATION_DIR = "animations"
# VIDEO_DIR = "media/videos/generated_scene/1080p15"
# os.makedirs(ANIMATION_DIR, exist_ok=True)
# os.makedirs(VIDEO_DIR, exist_ok=True)

@app.route('/')
def home():
    return "Server is running!"

ANIMATION_DIR = "animations"
OUTPUT_FILENAME = "output.mp4"
MEDIA_DIR = "media"
VIDEO_PATH = os.path.join(MEDIA_DIR, "videos", "generated_scene", "1080p15", OUTPUT_FILENAME)

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

        scene_file = os.path.join(ANIMATION_DIR, "generated_scene.py")
        os.makedirs(ANIMATION_DIR, exist_ok=True)
        with open(scene_file, "w") as f:
            f.write(code)

        match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\):', code)
        if not match:
            return jsonify({"error": "No Scene class found in code"}), 400
        scene_name = match.group(1)

        # Run Manim with forced output directory
        subprocess.run([
            "manim", "-pql", scene_file, scene_name,
            "-o", OUTPUT_FILENAME, "-r", "1920,1080",
            "--media_dir", MEDIA_DIR
        ], check=True)

        return jsonify({
            "video_url": f"http://localhost:5000/get_video"
        })

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Manim rendering failed: {e}"}), 500
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/retry', methods=['POST'])
def retry_generation():
    data = request.json
    prompt = data.get('prompt')
    error_msg = data.get('errorMessage')

    try:
        fixed_code = get_fixed_code(prompt, error_msg)

        match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\):', fixed_code)
        if not match:
            return jsonify({"error": "No Scene class in fixed code"}), 400
        scene_name = match.group(1)

        with open(os.path.join(ANIMATION_DIR, "generated_scene.py"), "w") as f:
            f.write(fixed_code)

        subprocess.run([
            "manim", "-pql", os.path.join(ANIMATION_DIR, "generated_scene.py"),
            scene_name, "-o", "output.mp4", "-r", "1920,1080"
        ], check=True)

        return jsonify({
            "message": "Video regenerated successfully!",
            "video_url": "http://localhost:5000/videos/1080p60/output.mp4"
        })

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Manim retry rendering failed: {e}"}), 500
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# @app.route('/videos/1080p60/<path:filename>')
# def serve_1080p60_video(filename):
#     return send_from_directory("media/videos/generated_scene/1080p15", filename)

@app.route("/get_video", methods=["GET"])
def get_video():
    video_path = os.path.abspath("media/videos/generated_scene/1080p15/output.mp4")
    print("Trying to send video from:", video_path)

    if os.path.exists(video_path):
        return send_file(video_path, mimetype='video/mp4')
    
    return "Video not found", 404


def get_fixed_code(prompt, error_msg):
    system_message = {
        "role": "system",
        "content": (
        "You are an expert Python developer and animation engineer with deep knowledge of the Manim Community Edition (v0.18 or later).\n\n"
        "Your task is to fix the following Manim code so that it runs correctly without any syntax or runtime errors.\n\n"
        "Instructions:\n"
        "- Output MUST be valid and corrected Python code ONLY (no markdown formatting, no comments, no explanations).\n"
        "- Include necessary imports like:\n"
        "    from manim import *\n\n"
        "- Ensure the code defines a class named `GeneratedScene(Scene)`.\n"
        "- Fix any deprecated methods, incorrect parameters, or outdated syntax.\n"
        "- Use valid constructs like: Circle, Square, Text, Arrow, Line, Create, FadeIn, Transform, MoveToTarget, wait(), etc.\n"
        "- Do NOT include any extra text like 'Here is the corrected code'.\n"
        "- The fixed code must be compatible with Python 3.12 and ManimCE.\n"
        "- Output file will be saved as `animations/generated_scene.py`.\n"
        "- The scene must run with:\n"
        "    manim -pql animations/generated_scene.py GeneratedScene -o output.mp4\n\n"
        "Here is the code with errors:\n"
        "\"\"\"\n"
        "<BUGGY_MANIM_CODE_HERE>\n"
        "\"\"\"\n\n"
        "Output ONLY the corrected Python code including all necessary imports."
    )
    }

    user_message = {
        "role": "user",
        "content": f"""The prompt was:\n{prompt}\n\nThe error was:\n{error_msg}\n\nFix it and return only the fixed Python code."""
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": [system_message, user_message]
        }
    )

    result = response.json()
    code = result['choices'][0]['message']['content']
    code = re.sub(r"^```(?:python)?|```$", "", code, flags=re.MULTILINE).strip()
    return code

if __name__ == '__main__':
    app.run(debug=True)
