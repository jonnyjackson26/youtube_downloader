import React, { useState } from "react";
import axios from "axios";

function App() {
  const [url, setURL] = useState("");
  const [error, setError] = useState(null);

  const handleDownload = async () => {
    if (!url.trim()) {
      alert("Please enter a valid URL!");
      return;
    }

    try {
      const response = await axios.post("/download", {
        url,
      }, {
        responseType: "blob", // Ensures the file is treated as binary
      });

      const blob = new Blob([response.data], { type: "video/mp4" });
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = downloadUrl;
      link.download = "video.mp4"; // Default name; you can improve this
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (err) {
      console.error("Error downloading video:", err);
      setError("Failed to download the video.");
    }
  };

  return (
    <div style={{ padding: "1rem" }}>
      <h1>YouTube Downloader</h1>
      <input
        type="text"
        placeholder="Enter YouTube URL..."
        value={url}
        onChange={(e) => setURL(e.target.value)}
        style={{ padding: "0.5rem", width: "300px" }}
      />
      <button onClick={handleDownload} style={{ padding: "0.5rem", marginLeft: "10px" }}>
        Download
      </button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default App;
