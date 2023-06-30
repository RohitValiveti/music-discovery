import React, { useState, useEffect } from "react";
import { User } from "../types/user";
import { Link } from "react-router-dom";

const Homepage = () => {
  const [userInfo, setUserInfo] = useState<User | null>(null);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("/user/");
        const data = await response.json();
        setUserInfo(data);
      } catch (error) {
        console.error("Error:", error);
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      {userInfo ? (
        <div>
          <h2>Welcome!</h2>
          <p>Name: {userInfo.name}</p>
          <p>Followers: {userInfo.followers}</p>
          <p>Public Playlists: {userInfo.public_playlists}</p>
          <p>
            Top Tracks:
            {userInfo.top_tracks.map((track, idx) => (
              <li key={idx}>{track.name}</li>
            ))}
          </p>
          <Link to={"/chooseplaylist"}>Disover Music</Link>
        </div>
      ) : (
        <p>Loading user data...</p>
      )}
    </div>
  );
};

export default Homepage;
