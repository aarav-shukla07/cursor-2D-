import React from "react";
import PromptForm from "./components/PromptForm";
import "./styles/App.css";

function App(){
  return (
    <div className="app">
      <h1>Cursor 2D Animation Generator</h1>
      <PromptForm />
    </div>
    
  );
  
}

export default App;