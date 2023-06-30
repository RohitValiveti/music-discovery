import React, { useState, useEffect } from "react";

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
    <div>
      <h3>{name}</h3>
      <p>Album: {album}</p>
      {artists && (
        <p>
          Artist(s):{" "}
          {artists.map((artist) => (
            <p>{artist}</p>
          ))}
        </p>
      )}
      <button onClick={handleClick}>Add Track to your Playlist</button>
      {added && <div>Added to playlist!</div>}
      <br />
      <img src={album_img_url} alt="album" />
    </div>
  );
};

export default SongModal;
