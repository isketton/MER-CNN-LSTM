import "./Modal.css";
const Modal = ({ item, detailedData, onClose, isActive }) => {
  // ... modal content and styling logic

  return (
    <div className={`modal-popup ${isActive ? "active" : ""}`}>
      <div className="modal-content">
        <p>Title: {item.title}</p>
        <p>Artist: {item.artist}</p>
        <p>Arousal: {item.arousal}</p>
        <p>Valence: {item.valence}</p>
        <p>Top 5 Recommended:</p>
        <ul>
          {detailedData.map((song, index) => (
            <li key={index}>
              {song.title} - {song.artist}
            </li>
          ))}
        </ul>
        <button className="close-button" onClick={onClose}>×</button>
      </div>
    </div>
  );
};

export default Modal;
