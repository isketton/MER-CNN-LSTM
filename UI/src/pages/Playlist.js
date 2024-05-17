import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import Modal from "../components/Modal";
import "./Playlist.css";

const Playlist = () => {
  const [playlists, setPlaylists] = useState([]); // State to store playlists
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedEmotion, setSelectedEmotion] = useState("");
  const [selectedName, setSelectedName] = useState("");
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  const handleSelectChange = (e) => {
    setSelectedEmotion(e.target.value);
  };

  const fetchData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/api/playlists");
      setData(response.data);
      console.log(response.data);
    } catch (error) {
      setError(error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddPlaylist = async (playlistName) => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/api/home");
      const songs = response.data.map((song) => ({
        arousal: song.arousal,
        valence: song.valence,
        artist: song.artist,
        title: song.title,
        song_id: song.song_id,
      }));

      const filteredSongs = songs.filter((song) => {
        if (selectedEmotion === "happy") {
          return song.valence > 0.5 && song.arousal > 0.5;
        } else if (selectedEmotion === "sad") {
          return song.valence <= 0.5 && song.arousal <= 0.5;
        } else if (selectedEmotion === "angry") {
          return song.valence > 0.5 && song.arousal <= 0.5;
        } else if (selectedEmotion === "relaxed") {
          return song.valence <= 0.5 && song.arousal > 0.5;
        }
        return false;
      });

      await axios.post("http://127.0.0.1:5000/api/playlists_insert", {
        name: selectedName,
        songs: filteredSongs,
      });

      // Optimistically update local state before refetching from the server
      setPlaylists((prevPlaylists) => [
        ...prevPlaylists,
        { name: selectedName, songs: filteredSongs },
      ]);

      // Fetch updated data from the server
      await fetchData();
      closeModal();
    } catch (error) {
      console.error("Error adding playlist:", error);
    }
  };

  const handleDeletePlaylist = async (playlistId) => {
    try {
      await axios.delete(
        `http://127.0.0.1:5000/api/delete_playlist?playlist_id=${playlistId}`
      );
      setData(data.filter((playlist) => playlist.playlist_id !== playlistId));
      await fetchData();
    } catch (error) {
      console.error("Error deleting playlist:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <div className="playlists">
      <h1>Playlists</h1>
      <button className="plus-button" onClick={openModal}>
        +
      </button>
      <div className="grid-container">
        {data.map((item, index) => (
          <div key={index} className="grid-item">
            <button
              className="delete-button"
              onClick={() => handleDeletePlaylist(item.playlist_id)}
            >
              X
            </button>
            <Link to={`/playlist/${item.name}`} className="grid-item">
              <h2>{item.name}</h2>
              {item.song_ids && (
                <p>songs: {item.song_ids[0]?.split(",").length}</p>
              )}
            </Link>
          </div>
        ))}
      </div>
      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>Add New Playlist</h2>
            <input
              type="text"
              placeholder="Playlist Name"
              value={selectedName}
              onChange={(e) => setSelectedName(e.target.value)}
            />
            <select
              className="select-field"
              value={selectedEmotion}
              onChange={handleSelectChange}
            >
              <option value="">Select an emotion</option>
              <option value="happy">Happy</option>
              <option value="sad">Sad</option>
              <option value="angry">Angry</option>
              <option value="relaxed">Relaxed</option>
            </select>
            <button onClick={closeModal}>Cancel</button>
            <button onClick={handleAddPlaylist}>Add</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Playlist;
