import React, { useState, useEffect } from "react";
import { Playlist } from "../types/playlist";
import { Link } from "react-router-dom";
import {
  Box,
  Card,
  CardContent,
  CardMedia,
  IconButton,
  List,
  ListItem,
  Typography,
} from "@mui/material";
import SyncLoader from "react-spinners/SyncLoader";
import LastPage from "../components/LastPage";
import theme from "../types/Theme";
import SkipPreviousIcon from "@mui/icons-material/SkipPrevious";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import SkipNextIcon from "@mui/icons-material/SkipNext";

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
    <div style={{ color: "#535353" }}>
      {playlists.length !== 0 ? (
        <div>
          <LastPage endpoint={"/homepage"} pageName="homepage" />
          <div className="homepage">
            <Typography variant="h4" style={{ padding: 40 }}>
              Choose a playlist to generate recommendations from
            </Typography>
            <List className="playlist-list">
              {playlists.map((playlist) => (
                <ListItem disablePadding key={playlist.id}>
                  <Link
                    to={`/recommendations/${playlist.id}`}
                    style={{ color: "#212121", textDecoration: "none" }}
                  >
                    <Card className="playlist-card">
                      <Box sx={{ display: "flex", flexDirection: "column" }}>
                        <CardContent sx={{ flex: "1 0 auto" }}>
                          <Typography component="div" variant="h5">
                            {playlist.name}
                          </Typography>
                        </CardContent>
                        <Box className="playlist-box">
                          <IconButton aria-label="previous">
                            {theme.direction === "rtl" ? (
                              <SkipNextIcon />
                            ) : (
                              <SkipPreviousIcon />
                            )}
                          </IconButton>
                          <IconButton aria-label="play/pause">
                            <PlayArrowIcon sx={{ height: 38, width: 38 }} />
                          </IconButton>
                          <IconButton aria-label="next">
                            {theme.direction === "rtl" ? (
                              <SkipPreviousIcon />
                            ) : (
                              <SkipNextIcon />
                            )}
                          </IconButton>
                        </Box>
                      </Box>
                      <CardMedia
                        component="img"
                        sx={{ width: 151 }}
                        src={playlist.playlist_img_url}
                        alt={playlist.name}
                      />
                    </Card>
                  </Link>
                </ListItem>
              ))}
            </List>
          </div>
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
