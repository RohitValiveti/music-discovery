import React from "react";
import { Link } from "react-router-dom";

const Welcome = () => {
  return (
    <>
      <div>Welcome</div>
      <Link to={"/signin"}>Sign in to Spotify</Link>
    </>
  );
};

export default Welcome;
