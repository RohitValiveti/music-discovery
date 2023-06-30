import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { FullTrack } from "../types/track";

const Recommendations = () => {
  const { id } = useParams();
  const [tracks, setTracks] = useState<FullTrack[]>([]);
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

  return (
    <div>
      {tracks.length !== 0 ? (
        <div>
          <h2>Your Recommendations based on this Playlist!</h2>
          {tracks.map((track) => (
            <li key={track.id}>{track.name}</li>
            // Add modal popul for clicking on each title (Dont add new page or else navigating back to recs will cause re load)
          ))}
        </div>
      ) : (
        <p>Loading Recommendations...</p>
      )}
    </div>
  );
};

export default Recommendations;
