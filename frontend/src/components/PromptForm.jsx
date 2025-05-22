import React, { useState } from "react";
import axios from "axios";

const PromptForm = ({ setVideoURL, setVideoReady }) => {
    const [prompt, setPrompt] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleGenerate = async (e) => {
        e.preventDefault();
        setLoading(true);
        setVideoURL("");
        setError("");
        setVideoReady(false);

        try {
            const response = await axios.post("http://localhost:5000/generate", { prompt }, {
                responseType: "blob"
            });

            const blob = new Blob([response.data], { type: "video/mp4" });
            const videoBlobUrl = URL.createObjectURL(blob);

            setVideoURL(videoBlobUrl);
            setVideoReady(true);
        } catch (err) {
            const errMsg = err.response?.data?.error || err.message || "Unknown error occurred.";
            setError(errMsg);
        }

        setLoading(false);
    };

    return (
        <div className="input-wrapper">
            <form onSubmit={handleGenerate}>
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

            {error && (
                <div style={{ marginTop: "1rem", color: "red" }}>
                    <p><strong>Error:</strong> {error}</p>
                </div>
            )}
        </div>
    );
};

export default PromptForm;
