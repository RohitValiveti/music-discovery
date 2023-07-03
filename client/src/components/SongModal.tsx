import { useState, useEffect } from "react";

type SongModalPropType = {
  id?: string;
  album?: string;
  name?: string;
  artists?: string[];
  album_img_url?: string;
  playlist_id: string | undefined;
};

const SongModal = ({
  id,
  album,
  name,
  artists,
  playlist_id,
  album_img_url,
}: SongModalPropType) => {
  const [added, setAdded] = useState(false);
  useEffect(() => {
    setAdded(false);
  }, [id]);
  const handleClick = async () => {
    try {
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ track_id: id, playlist_id: playlist_id }),
      };
      await fetch("/add-track/", requestOptions);
      setAdded(true);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="music-panel">
      <div className="music-panel__content">
        <div className="music-panel__info">
          <h3 className="music-panel__title">{name}</h3>
          <p className="music-panel__album">Album: {album}</p>
          {artists && (
            <p className="music-panel__artists">
              Artist(s):{" "}
              {artists.map((artist, index) => (
                <span key={index} className="music-panel__artist">
                  {artist},
                </span>
              ))}
            </p>
          )}
          <button className="music-panel__button" onClick={handleClick}>
            Add Track to your Playlist
          </button>
          {added && (
            <div className="music-panel__message">Added to playlist!</div>
          )}
        </div>
        <img className="music-panel__image" src={album_img_url} alt="album" />
      </div>
    </div>
  );
};

export default SongModal;
