import React, { useState, useEffect } from "react";
import { Playlist } from "../types/playlist";
import { Link } from "react-router-dom";
import { Typography } from "@mui/material";
import SyncLoader from "react-spinners/SyncLoader";

const ChoosePlaylist = () => {
  const [playlists, setPlaylists] = useState<Playlist[]>([]);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("/playlists/");
        const data = await response.json();
        setPlaylists(data.playlists);
      } catch (error) {
        console.error("Error:", error);
      }
    };
    fetchData();
  }, []);

  return (
    <>
      <div>
        {playlists.length !== 0 ? (
          <div>
            <h2>Choose A Playlist to generate Recommendations From!</h2>
            {playlists.map((playlist) => (
              <li key={playlist.id}>
                <Link to={`/recommendations/${playlist.id}`}>
                  {playlist.name}
                </Link>
              </li>
            ))}
          </div>
        ) : (
          <Typography
            variant="h6"
            className="loader"
            style={{ color: "#535353" }}
          >
            <SyncLoader color="#1db954" />
            Loading Playlists
          </Typography>
        )}
      </div>
    </>
  );
};

export default ChoosePlaylist;
