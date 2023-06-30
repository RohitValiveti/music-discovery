import Signin from "../pages/Signin";
import Homepage from "../pages/Homepage";
import Welcome from "../pages/Welcome";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ChoosePlaylist from "../pages/ChoosePlaylist";
import Recommendations from "../pages/Recommendations";

const Router = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route index element={<Welcome />}></Route>
        <Route path="/welcome" element={<Welcome />}></Route>
        <Route path="/signin" element={<Signin />}></Route>
        <Route path="/homepage" element={<Homepage />}></Route>
        <Route path="/chooseplaylist" element={<ChoosePlaylist />}></Route>
        <Route
          path="/recommendations/:id"
          element={<Recommendations />}
        ></Route>
      </Routes>
    </BrowserRouter>
  );
};

export default Router;
