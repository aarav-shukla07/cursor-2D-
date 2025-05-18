import os
import subprocess

def generate_video(script_path, resolution='1080p60'):
    output_dir = f'media/videos/{resolution}'
    os.makedirs(output_dir, exist_ok=True)

    command = [
        "manim",
        script_path,
        "FormationOfCube",
        "-qk" if resolution == "480p15" else "-qm" if resolution == "480p30" else "-qh",
        "--output_file", "cube_formation.mp4"
    ]

    subprocess.run(command, check=True)

    return os.path.join(output_dir, "cube_formation.mp4")