import React from "react";
import PromptForm from "./components/PromptForm";
import VideoPlayer from "./components/VideoPlayer"; 
import "./styles/App.css";

function App(){
  return (
    <div className="app">
      <h1>Cursor 2D Animation Generator</h1>
      <PromptForm />
      <VideoPlayer />
    </div>
  );
}

export default App;