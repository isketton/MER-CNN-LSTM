import { useParams } from "react-router-dom";
import "./Home.css";
import React, { useState, useEffect } from "react";
import axios from "axios";
const PlaylistSongs = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState([]);
  const { playlistName } = useParams();
  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/api/playlists_songs?name=${playlistName}`,
          {}
        );
        setData(res.data);
        console.log(res.data);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [playlistName]);
  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <div className="home-container">
      <div className="grid-container">
        {/* Render filtered data instead of all data */}
        {data.map((item, index) => (
          <div key={index} className="grid-item">
            <p>{item.title}</p>
            <p>{item.artist}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PlaylistSongs;
