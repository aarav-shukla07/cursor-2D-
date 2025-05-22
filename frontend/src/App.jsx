import React, { useState } from "react";
import PromptForm from "./components/PromptForm";
import "./styles/App.css";

function App() {
  const [videoURL, setVideoURL] = useState("");
  const [videoReady, setVideoReady] = useState(false);
  const [hasGenerated, setHasGenerated] = useState(false);

  return (
    <div className="app">
      {hasGenerated && <div className="header">Cursor-2D</div>}

      {!hasGenerated && (
        <div className="welcome-message">
          <h1>Welcome to Cursor-2D Animation</h1>
        </div>
      )}

      <PromptForm
        setVideoURL={(url) => {
          setVideoURL(url);
          setHasGenerated(true);
        }}
        setVideoReady={setVideoReady}
      />

      <div className="chat-container">
        {videoReady && (
          <>
            <div className="video-wrapper">
              <video src={videoURL} controls autoPlay muted  style={{width: "600px", borderRadius: "10px",  boxShadow: "0 0 10px rgba(0, 0, 0, 0.5)"}}/>
              <a href={videoURL} download="cursor2d_video.mp4" className="download-button">
                Download Video
              </a>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
