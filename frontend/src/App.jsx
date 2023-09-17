import React from "react";
import Navbar from "./Components/Navbar";
import Leaderboard from "./Leaderboard";
import ListBoards from "./Components/ListBoards";
import Home from "./Home";
import Signup from "./Signup";
import "./index.css";
import { Route, Routes, Link } from "react-router-dom";

function App() {
  return (
    <>
      <React.Fragment>
        <Navbar />
      </React.Fragment>

      <div class="container"></div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/Components/ListBoards" element={<ListBoards />} />
        <Route path="/Signup" element={<Signup />} />
      </Routes>
    </>
  );
}

export default App;
