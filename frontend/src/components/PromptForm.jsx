import React, { useState } from "react";

const PromptForm = ({ onSendPrompt, loading }) => {
  const [prompt, setPrompt] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    onSendPrompt(prompt);
    setPrompt("");
  };

  return (
    <div className="input-wrapper">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter your prompt..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <button type="submit" disabled={loading}>
          {loading ? "..." : "→"}
        </button>
      </form>
    </div>
  );
};

export default PromptForm;
