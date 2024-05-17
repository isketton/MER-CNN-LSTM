import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Home.css";
import { Link } from "react-router-dom";
import Modal from "../components/Modal";

const Home = () => {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedGridItem, setSelectedGridItem] = useState(null);
  const [isActive, setIsActive] = useState(false);
  const [searchQuery, setSearchQuery] = useState(""); // State for search query
  const [detailedData, setDetailedData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/home", {});
        setData(response.data);
        console.log(response.data);
        setFilteredData(response.data); // Initialize filteredData with all data
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    // Apply filtering logic when search query changes
    filterData();
  }, [searchQuery]);

  const filterData = () => {
    // Filter data based on search query
    const filtered = data.filter((item) => {
      const titleMatch = item.title
        .toLowerCase()
        .includes(searchQuery.toLowerCase());
      const artistMatch = item.artist
        .toLowerCase()
        .includes(searchQuery.toLowerCase());
      const emotionMatch = mapEmotion(item.arousal, item.valence)
        .toLowerCase()
        .includes(searchQuery.toLowerCase());
      return titleMatch || artistMatch || emotionMatch;
    });
    setFilteredData(filtered);
  };

  const handleSearchInputChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleDeletePlaylist = async (songId) => {
    try {
      await axios.delete(
        `http://127.0.0.1:5000/api/delete_song?song_id=${songId}`
      );
      setData(data.filter((song) => song.song_id !== songId));
      setFilteredData(filteredData.filter((song) => song.song_id !== songId));
    } catch (error) {
      console.error("Error deleting song:", error);
    }
  };

  const handleGridItemClicked = async (item) => {
    setSelectedGridItem(item); // Update selected item state
    const response = await axios.get(
      `http://127.0.0.1:5000/api/recommend/${item.song_id}`
    );
    setDetailedData(response.data);
    setIsActive(true);
  };

  const closeModal = () => {
    setSelectedGridItem(null); // Clear selected item state to close modal
    setIsActive(false);
  };

  const mapEmotion = (arousal, valence) => {
    if (arousal > 0.5 && valence > 0.5) {
      return "Happy";
    } else if (arousal > 0.5 && valence <= 0.5) {
      return "Angry";
    } else if (arousal <= 0.5 && valence > 0.5) {
      return "Relaxed";
    } else {
      return "Sad/Dark Vibes";
    }
  };

  const getColorForEmotion = (emotion) => {
    switch (emotion) {
      case "Happy":
        return "orange"; // Change color for Happy emotion
      case "Angry":
        return "red"; // Change color for Angry emotion
      case "Relaxed":
        return "green"; // Change color for Relaxed emotion
      case "Sad":
        return "blue"; // Change color for Sad emotion
      default:
        return "black"; // Default color
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }
  return (
    <div className="home-container">
      {/* Search Input */}
      <input
        className="search-bar"
        type="text"
        placeholder="Search by title, artist, or emotion..."
        value={searchQuery}
        onChange={handleSearchInputChange}
      />

      <div className="grid-container">
        {/* Render filtered data instead of all data */}
        {filteredData.map((item, index) => (
          <button
            key={index}
            className="grid-item"
            onClick={() => handleGridItemClicked(item)}
          >
            <button
              className="delete-button1"
              onClick={(e) => {e.stopPropagation(); 
                handleDeletePlaylist(item.song_id);}}
            >
              X
            </button>
            <p>{item.title}</p>
            <p>{item.artist}</p>
            <p
              className="emotion-bubble"
              style={{
                backgroundColor: getColorForEmotion(
                  mapEmotion(item.arousal, item.valence)
                ),
              }}
            >
              {mapEmotion(item.arousal, item.valence)}
            </p>
          </button>
        ))}
      </div>
      {selectedGridItem && detailedData && (
        <Modal
          item={selectedGridItem}
          detailedData={detailedData}
          onClose={closeModal}
          isActive={isActive}
        />
      )}
    </div>
  );
};

export default Home;
