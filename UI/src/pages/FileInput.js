import React, { useState } from "react";
import "./FileInput.css";
import axios from "axios";

export const FileInput = () => {
  const [selectedFiles, setSelectedFiles] = useState(null);
  const [predictionResult, setPredictionResult] = useState();
  const [title, setTitle] = useState(""); // State for title input
  const [artist, setArtist] = useState("");
  const [error, setError] = useState(""); // State for error message

  const handleFileChange = (e) => {
    setSelectedFiles(e.target.files[0]);
  };

  const handleFileDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type === "audio/mpeg") {
      setSelectedFiles(file);
    }
  };

  const handleFileSelect = (e) => {
    e.preventDefault();
    const files = e.target.files[0];
    setSelectedFiles(files);
  };

  const handleFileSelection = () => {
    const input = document.createElement("input");
    input.type = "file";
    input.directory = true;
    input.multiple = true;
    input.accept = ".mp3";
    input.addEventListener("change", handleFileSelect);
    input.click();
  };

  const handlePrediction = () => {
    if (!selectedFiles) {
      setError("Please select a file for prediction.");
      return;
    }
    if (!title.trim() || !artist.trim()) {
      setError("Please enter both title and artist.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFiles);
    formData.append("title", title); // Add title to form data
    formData.append("artist", artist);

    axios
      .post("http://127.0.0.1:5000/api/convert", formData)
      .then((response) => {
        console.log(response.data);
        setPredictionResult(response.data);
      })
      .catch((error) => {
        console.error(error);
        if (error.response && error.response.data) {
          setError(error.response.data.message);
        } else {
          setError("An error occurred during prediction.");
        }
      })
      .finally(() => {
        setSelectedFiles(null);
        setTitle("");
        setArtist("");
        setError(""); // Clear error message
      });
  };

  return (
    <div className="container">
      <div className="file-drop-container">
        <div
          className="file-drop"
          onDrop={handleFileDrop}
          onDragOver={(e) => e.preventDefault()}
        >
          Drag MP3 files here
        </div>
        <input
          className="file-input"
          type="file"
          accept=".mp3"
          multiple
          onChange={handleFileSelection}
        />
        <button className="folder-btn" onClick={handleFileSelection}>
          Select MP3 File
        </button>

        {selectedFiles && (
          <div>
            <h2>Selected File:</h2>
            <ul>
              <li key={selectedFiles.name}>{selectedFiles.name}</li>
            </ul>
            <label htmlFor="title">Title:</label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
            <label htmlFor="artist">Artist:</label>
            <input
              id="artist"
              type="text"
              value={artist}
              onChange={(e) => setArtist(e.target.value)}
            />
          </div>
        )}

        {error && <div className="error-message">{error}</div>}

        <button className="predict" onClick={handlePrediction}>Predict!</button>
        {predictionResult && (
          <div>
            <h2>Prediction Result:</h2>
            <pre>{JSON.stringify(predictionResult, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
};
