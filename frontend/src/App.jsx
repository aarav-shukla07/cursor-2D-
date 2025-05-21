import React, { useState } from "react";
import PromptForm from "./components/PromptForm";
import VideoPlayer from "./components/VideoPlayer";
import "./styles/App.css";

function App() {

  const [videoURL, setVideoURL] = useState("");
  const [videoReady, setVideoReady] = useState(false);
  return (
    <div className="app">
      <h1>Cursor 2D Animation Generator</h1>
      <PromptForm setVideoURL={setVideoURL} setVideoReady={setVideoReady} />
      {videoReady && videoURL && (
        <video width="800" height="450" controls autoPlay>
          <source src={videoURL} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      )}

    </div>
  );
}

export default App;