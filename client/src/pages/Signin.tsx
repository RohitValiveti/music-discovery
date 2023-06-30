import React from "react";

const Signin = () => {
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
  return <button onClick={handleClick}>Open Link</button>;
};

export default Signin;
