import React, { useState, useEffect } from "react";
import { Playlist } from "../types/playlist";
import { Link } from "react-router-dom";
import {
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Typography,
} from "@mui/material";
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
    <div className="homepage" style={{ color: "#535353" }}>
      {playlists.length !== 0 ? (
        <div>
          <Typography variant="h4" style={{ padding: 40 }}>
            Choose A Playlist to generate Recommendations From!
          </Typography>
          <List
            style={{
              display: "grid",
              justifyContent: "center",
              alignItems: "center",
              padding: 20,
            }}
          >
            {playlists.map((playlist) => (
              <ListItem disablePadding key={playlist.id}>
                <Link
                  to={`/recommendations/${playlist.id}`}
                  style={{ color: "#212121", textDecoration: "none" }}
                >
                  <ListItemButton>
                    <ListItemText
                      primary={playlist.name}
                      style={{ fontSize: 40 }}
                    />
                  </ListItemButton>
                </Link>
              </ListItem>
            ))}
          </List>
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
  );
};

export default ChoosePlaylist;
