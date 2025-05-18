def get_animation_script(prompt):
    if "cube" in prompt.lower():
        return "animations/formation_of_cube.py"
    
    return "anaimations/default_fallback.py"