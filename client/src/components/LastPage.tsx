import React from "react";
import FastRewindIcon from "@mui/icons-material/FastRewind";
import { Link } from "react-router-dom";

type LastPagePropType = {
  endpoint: string;
  pageName: string;
};

const LastPage = ({ endpoint, pageName }: LastPagePropType) => {
  return (
    <Link
      to={endpoint}
      style={{
        color: "#1db954",
        textDecoration: "none",
        border: "1px solid #1db954",
        borderRadius: "4px",
        padding: "8px",
        marginBottom: "8px",
        cursor: "pointer",
        display: "inline-block",
        marginRight: "10px",
      }}
    >
      <FastRewindIcon
        fontSize="large"
        style={{
          position: "absolute",
          top: "10px",
          left: "35px",
          cursor: "pointer",
        }}
      />
      <br></br>
      <br></br>
      <div>
        <strong>Back to {pageName}</strong>
      </div>
    </Link>
  );
};

export default LastPage;
