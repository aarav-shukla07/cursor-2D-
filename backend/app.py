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
                        """
You are a senior Python developer with expertise in Manim (Community Edition v0.18 or later), mathematics, physics, and data visualization.

Your task is to generate a fully working Manim animation script based on the user's request.

STRICT INSTRUCTIONS:
- Output must be valid Python code ONLY — no explanations, markdown, or commentary.
- Always begin the script with:
    from manim import *
    
- Use the latest ManimCE v0.18+ features and syntax.
- Use additional imports (e.g., math, numpy, manim_physics) as needed depending on the user’s prompt.
- Define exactly ONE scene class, always named:
    class GeneratedScene(Scene):
- Use only standard ManimCE v0.18+ methods (Create, FadeIn, Write, MoveToTarget, wait(), etc.).
- If physics is involved, import from manim_physics (e.g., from manim_physics import *). Use only if necessary.
- Ensure the animation runs with:
    manim -pql animations/generated_scene.py GeneratedScene -o output.mp4
- The code must prevent overlapping visuals: text or math objects should appear sequentially, or fade out before new content appears.
- Avoid visual clutter. Use `FadeOut` or `.next_to()` or `.shift()` to clearly separate elements.
- The animation should be clean, functional, and visually engaging.

USER PROMPT:
\"\"\"
<USER_ANIMATION_REQUEST_HERE>
\"\"\"
"""
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
