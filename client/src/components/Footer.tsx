import React from "react";
import { Typography, Link, Box } from "@mui/material";
import GitHubIcon from "@mui/icons-material/GitHub";
import LinkedInIcon from "@mui/icons-material/LinkedIn";

const Footer = () => {
  return (
    <Box component="footer" className="footer">
      <Link
        href="https://rohitvaliveti.github.io"
        target="_blank"
        rel="noopener noreferrer"
        color="inherit"
        sx={{ mr: 2 }}
      >
        <Typography variant="body2" sx={{ mr: 2 }}>
          Created by Rohit Valiveti
        </Typography>
      </Link>
      <Link
        href="https://github.com/RohitValiveti"
        target="_blank"
        rel="noopener noreferrer"
        color="inherit"
        sx={{ mr: 2 }}
      >
        <GitHubIcon />
      </Link>
      <Link
        href="https://www.linkedin.com/in/rohitvaliveti/"
        target="_blank"
        rel="noopener noreferrer"
        color="inherit"
      >
        <LinkedInIcon />
      </Link>
    </Box>
  );
};

export default Footer;
