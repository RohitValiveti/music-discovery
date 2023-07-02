import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { FullTrack } from "../types/track";
import SongModal from "../components/SongModal";
import SyncLoader from "react-spinners/SyncLoader";
import { Typography } from "@mui/material";
import LastPage from "../components/LastPage";

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
        const data = await response.json();
        setTracks(data.recs);
      } catch (error) {
        console.error("Error:", error);
      }
    };
    fetchData();
  }, [id]);

  const onItemClick = (track: FullTrack) => {
    setSelectedTrack(track);
    setShowModal(true);
  };

  const handleMouseEnter = (e: React.MouseEvent<HTMLLIElement>) => {
    const liElement = e.target as HTMLLIElement;
    liElement.style.backgroundColor = "#b3b3b3";
  };

  const handleMouseLeave = (e: React.MouseEvent<HTMLLIElement>) => {
    const liElement = e.target as HTMLLIElement;
    liElement.style.backgroundColor = "#fff";
  };

  return (
    <div>
      {tracks.length !== 0 ? (
        <div>
          <LastPage endpoint={"/choosePlaylists"} pageName="playlists" />
          <div className="homepage" style={{ color: "#535353" }}>
            <Typography variant="h3" style={{ padding: 20 }}>
              Your Recommendations based on <strong>PLAYLIST</strong>
            </Typography>
            <ul style={{ listStyleType: "none", padding: 0 }}>
              {tracks.map((track) => (
                <li
                  className="rec-item"
                  key={track.id}
                  onClick={() => onItemClick(track)}
                  style={{
                    border: "1px solid #1db954",
                    borderRadius: "4px",
                    padding: "8px",
                    marginBottom: "8px",
                    cursor: "pointer",
                    display: "inline-block",
                    marginRight: "10px",
                  }}
                  onMouseEnter={handleMouseEnter}
                  onMouseLeave={handleMouseLeave}
                >
                  {track.name}
                </li>
              ))}
            </ul>
          </div>
          {showModal && <SongModal {...selectedTrack} playlist_id={id} />}
        </div>
      ) : (
        <Typography
          variant="h6"
          className="loader"
          style={{ color: "#535353" }}
        >
          <SyncLoader color="#1db954" />
          Generating Recommendations
        </Typography>
      )}
    </div>
  );
};

export default Recommendations;
