import React, { useState } from "react";
import PromptForm from "./components/PromptForm";
import "./styles/App.css";

function App() {
  const [videoURL, setVideoURL] = useState("");
  const [videoReady, setVideoReady] = useState(false);

  return (
    <div className="app">
  <h1>Cursor 2D Animation Generator</h1>
  <PromptForm setVideoURL={setVideoURL} setVideoReady={setVideoReady} />
  <div className="chat-container">
    {videoReady && (
      <>
        <div className="chat-bubble user-message">
          { /* Replace this if you want to show the prompt */ }
          {prompt}
        </div>
        <div className="chat-bubble bot-message">
          <video src={videoURL} controls autoPlay muted />
        </div>
      </>
    )}
  </div>
</div>

  );
}

export default App;
