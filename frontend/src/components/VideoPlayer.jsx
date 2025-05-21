import React from "react";

const VideoPlayer = () => {
  return (
    <div>
      <h2>Animation Preview</h2>
      <video width="640" height="480" controls>
        <source src="http://localhost:5000/get_video" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  );
};

export default VideoPlayer;
