import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: {
      main: "#1db954", // Green
    },
    secondary: {
      main: "#212121", // Lighter Black
    },
    error: {
      main: "#121212", // Black
    },
    warning: {
      main: "#535353", // Gray
    },
    info: {
      main: "#b3b3b3", // Light Gray
    },
  },
});

export default theme;
