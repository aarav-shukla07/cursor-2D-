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
            const response = await axios.post("http://localhost:5000/generate", { prompt });
            const url = response.data.video_url;
            if (!url) throw new Error("Video URL not returned from backend");

            setVideoURL(`${url}?t=${Date.now()}`);
            setVideoReady(true);
        } catch (err) {
            const errMsg = err.response?.data?.error || err.message || "Unknown error occurred.";
            setError(errMsg);
        }

        setLoading(false);
    };

    const handleRetry = async () => {
        setLoading(true);
        setVideoURL("");
        setVideoReady(false);

        try {
            const retryResponse = await axios.post("http://localhost:5000/retry", {
                prompt,
                errorMessage: error,
            });

            const url = retryResponse.data.video_url;
            if (!url) throw new Error("Retry succeeded but video URL missing");

            setVideoURL(url);
            setVideoReady(true);
            setError("");
        } catch (retryErr) {
            const retryMsg = retryErr.response?.data?.error || retryErr.message || "Retry failed.";
            setError(retryMsg);
        }

        setLoading(false);
    };

    return (
        <div>
            <form onSubmit={handleGenerate}>
                <input
                    type="text"
                    placeholder="Enter your prompt..."
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                />
                <button type="submit" disabled={loading}>
                    {loading ? "Generating..." : "Generate"}
                </button>
            </form>

            {error && (
                <div style={{ marginTop: "1rem", color: "red" }}>
                    <p><strong>Error:</strong> {error}</p>
                    <button onClick={handleRetry} disabled={loading}>
                        {loading ? "Retrying..." : "Retry Fix"}
                    </button>
                </div>
            )}
        </div>
    );
};

export default PromptForm;
