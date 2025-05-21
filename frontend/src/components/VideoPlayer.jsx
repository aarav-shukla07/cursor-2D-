import React from "react";

const VideoPlayer = ({ videoURL }) => {
  return (
    <div style={{ marginTop: "1rem" }}>
      <video src={videoURL} controls autoPlay muted width="480" />
    </div>
  );
};

export default VideoPlayer;
