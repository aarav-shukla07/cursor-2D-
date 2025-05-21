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
      {videoReady && (
  <video
    src="http://localhost:5000/get_video"
    controls
    style={{ width: "100%", maxWidth: "720px", marginTop: "20px" }}
  />
)}

    </div>
  );
}

export default App;