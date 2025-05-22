import React, { useState } from "react";
import PromptForm from "./components/PromptForm";
import "./styles/App.css";

function App() {
  const [videoURL, setVideoURL] = useState("");
  const [videoReady, setVideoReady] = useState(false);
  const [hasGenerated, setHasGenerated] = useState(false);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSendPrompt = async (promptText) => {
    setMessages((prev) => [...prev, { type: "user", text: promptText }]);
    setLoading(true);
    setHasGenerated(true);
    setVideoReady(false);
    setVideoURL("");

    // Show "Generating video..." only while loading
    setMessages((prev) => [...prev, { type: "bot", text: "Generating video..." }]);

    try {
      const response = await fetch("http://localhost:5000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: promptText }),
      });

      const blob = await response.blob();
      const videoBlobUrl = URL.createObjectURL(blob);

      // Replace "Generating video..." message with video
      setMessages((prev) =>
        prev.filter((msg) => msg.text !== "Generating video...")
      );
      setVideoURL(videoBlobUrl);
      setVideoReady(true);
    } catch (err) {
      setMessages((prev) => [
        ...prev.filter((msg) => msg.text !== "Generating video..."),
        { type: "bot", text: "Error generating video." },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="app">
      {!hasGenerated && (
        <div className="welcome-message">
          <h1>Welcome to Cursor-2D Animation</h1>
        </div>
      )}

      {hasGenerated && <div className="header">Cursor-2D</div>}

      <div className="chat-container">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-bubble ${msg.type}`}
            style={
              msg.type === "user"
                ? { marginLeft: "50px", alignSelf: "flex-end" }
                : { marginRight: "400px", alignSelf: "flex-start" }
            }
          >
            {msg.text}
          </div>
        ))}

        {videoReady && (
          <div
            className="chat-bubble bot"
            style={{ marginRight: "50px", alignSelf: "flex-start", boxShadow: "none" }}
          >
            <video
              src={videoURL}
              controls
              autoPlay
              muted
              style={{
                width: "600px",
                borderRadius: "10px",
                boxShadow: "0 0 10px rgba(0, 0, 0, 0.5)",
              }}
            />
            <a
              href={videoURL}
              download="cursor2d_video.mp4"
              className="download-button"
            >
              Download Video
            </a>
          </div>
        )}
      </div>

      <PromptForm onSendPrompt={handleSendPrompt} loading={loading} />
    </div>
  );
}

export default App;
