# Cursor-2D Animation Generator

Cursor-2D is a web app that turns natural language prompts into 2D animations using [ManimCE](https://www.manim.community/), powered by LLM-generated code.
It would let users to create rich, animated scenes directly in the browser without writing any code.

### Landing Page
![Screenshot from 2025-05-23 11-46-12](https://github.com/user-attachments/assets/5c3c786a-47be-4eb3-b325-8cec390beeb8)

### Chat interface
![Screenshot from 2025-05-23 11-56-32](https://github.com/user-attachments/assets/90fa96fa-666f-4ade-a6d6-05562336fbe8)

### Sample Video Output image
![Screenshot from 2025-05-23 12-01-25](https://github.com/user-attachments/assets/c3f47a34-ed96-479c-a235-4ca8e37c1d43)

---

##  Features

- Prompt-to-animation via AI
- React-based chat interface
- No need of writing code to get animations
- Manim video rendering on the fly
- Downloadable animations
- Background loop video before user input
- Chat-Style Interaction

---

## Getting Started

### 1. Clone the repository

```bash

git clone https://github.com/your-username/cursor-2d.git
cd cursor-2D-
```

### 2. Install Dependencies

Backend (Flask + OpenRouter API + Manim)


```bash!

cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -U manim

```
Frontend (React + Vite)
```bash
cd ../frontend
npm install

```
### 3. Configure Environment
Paste the "meta-llama/llama-3-8b-instruct" api key generated from openrouter.ai in .env file
```bash
# backend/.env
OPENROUTER_API_KEY=your_openrouter_api_key

```
Tip: Never Commit your .env file
### 4. Run the App
Backend (Flask server)
```bash
cd backend
python app.py
```
Frontend (Vite dev server)
```bash
cd ../frontend
npm run dev
```

## 🗂️ Folder Structure
```
cursor-2D-/
├── backend/
│   ├── animations/                  # Stores generated Manim scenes
        ├── generated_scene.py          # Script to run generated animation
│   ├── media/                       # Output video & intermediate files
│   │   ├── images/                  # Generated images from scenes (if any)
│   │   ├── texts/                   # Any text content or temp files
│   │   └── videos/generated_scene/
│   │       ├── partial_movie_files/  # Intermediary Manim video fragments
│   │       └── output.mp4            # Final rendered video
│   ├── app.py                      # Flask server entry point
│   └── .env                        # API key config (do not commit)
├── frontend/
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   │   └── cursor.mp4          # Background looping video
│   │   ├── components/
│   │   │   ├── PromptForm.jsx      # Input form component for entering prompts
│   │   │   └── VideoPlayer.jsx     # Component for playing and downloading generated videos
│   │   ├── styles/
│   │   │   └── App.css             # Main CSS file for styling app components
│   │   ├── App.jsx                 # Main app layout and logic handling chat flow and state
│   │   ├── index.js                # Entry point for React app
│   │   └── main.jsx
│   ├── .gitignore
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md


```
## Example Prompts
- Show a square slowly fading in and rotating
- Generate Circle from triangle
- Display a circle expanding and contracting at center
- Solve the equation 2x = 6 step-by-step, showing each step as a new line
- Write 'Hello', then 'World', then fade both out

## Requirements
- Python 3.8+
- Node.js 16+
- ManimCE 0.18+

## 🙌 Contributing
Pull requests and feature ideas are welcome!

## 👤 Author

**Aarav Shukla**  
[GitHub](https://github.com/aarav-shukla07) • [LinkedIn](https://www.linkedin.com/in/aarav-shukla10/) • [Email](aarav10shukla@gmail.com) • [Twitter](https://x.com/aaravshukla_10) 
