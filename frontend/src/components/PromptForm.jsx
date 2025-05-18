import React, {useState} from "react";
import axios from "axios";

const PromptForm = () => {
    const [prompt, setPrompt] = useState("");
    const [videoURL, setVideoURL] = useState("");
    const [loading, setLoading] = useState(false);

    const handleGenerate = async (e) => {
        e.preventDefault();
        setLoading(true);
        setVideoURL("");

        try {
            const response = await axios.post("http://localhost:5000/generate", { prompt });
            setVideoURL(`http://localhost:5000${response.data.video_path}`);
        } catch (error) {
            alert("Error generating video");
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

            {videoURL && (
                <div className="video-container">
                    <video src={videoURL} controls width="480" />
                </div>
            )}
        </div>
    );
};

export default PromptForm;