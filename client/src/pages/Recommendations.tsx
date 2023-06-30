import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { FullTrack } from "../types/track";
import SongModal from "../components/SongModal";

const Recommendations = () => {
  const { id } = useParams();
  const [tracks, setTracks] = useState<FullTrack[]>([]);
  const [selectedTrack, setSelectedTrack] = useState<FullTrack | null>(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ playlist_id: id }),
        };
        const response = await fetch("/recommend/", requestOptions);
        console.log(response);
        const data = await response.json();
        setTracks(data.recs);
      } catch (error) {
        console.error("Error:", error);
      }
    };
    fetchData();
  }, []);

  const onItemClick = (track: FullTrack) => {
    setSelectedTrack(track);
    setShowModal(true);
  };

  return (
    <div>
      {tracks.length !== 0 ? (
        <div>
          <h2>Your Recommendations based on this Playlist!</h2>
          {tracks.map((track) => (
            <li key={track.id} onClick={() => onItemClick(track)}>
              {track.name}
            </li>
          ))}
          {showModal && <SongModal {...selectedTrack} playlist_id={id} />}
        </div>
      ) : (
        <p>Loading Recommendations...</p>
      )}
    </div>
  );
};

export default Recommendations;
