import Signin from "../pages/Signin";
import Homepage from "../pages/Homepage";
import Welcome from "../pages/Welcome";
import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";

const Router = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route index element={<Welcome />}></Route>
        <Route path="/welcome" element={<Welcome />}></Route>
        <Route path="/signin" element={<Signin />}></Route>
        <Route path="/homepage" element={<Homepage />}></Route>
      </Routes>
    </BrowserRouter>
  );
};

export default Router;
