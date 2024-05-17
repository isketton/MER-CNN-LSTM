import React from "react";
import Navbar from "./components/Navbar/index.js";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home.js";
import { FileInput } from "./pages/FileInput";
import Playlist from "./pages/Playlist";
import PlaylistSongs from "./pages/PlaylistSongs";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/home" element={<Home />} />
        <Route path="/fileinput" element={<FileInput />} />
        <Route path="/playlist" element={<Playlist />} />
        <Route path="/playlist/:playlistName" element={<PlaylistSongs />} />
      </Routes>
    </Router>
  );
}

export default App;
