import { Button, ThemeProvider, Typography } from "@mui/material";
import React from "react";
import { Link } from "react-router-dom";
import theme from "../types/Theme";
import "./styles.css";
const Welcome = () => {
  const handleClick = () => {
    fetch("/signin")
      .then((response) => response.json())
      .then((data) => {
        const link = data.sign_in_link;
        if (link) {
          // Open the link in a new tab or window
          window.open(link);
        } else {
          // Redirect to the homepage
          window.location.href = "/homepage";
        }
      })
      .catch((error) => {
        console.error(error);
      });
  };
  return (
    <div className="container" style={{ color: "#535353" }}>
      <Typography variant="h3" className="elt">
        Spotify Music Recommender
      </Typography>
      <Typography variant="h5" className="elt">
        Generate Personalized recommendations from your Spotify playlists!
      </Typography>
      <ThemeProvider theme={theme}>
        <Button
          variant="contained"
          color="primary"
          className="elt"
          onClick={handleClick}
          style={{ color: "white" }}
        >
          Sign in to Spotify
        </Button>
      </ThemeProvider>
    </div>
  );
};

export default Welcome;
