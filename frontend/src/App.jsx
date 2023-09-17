import React from "react";
import Navbar from "./Components/Navbar";
import Leaderboard from "./Leaderboard";
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
        <Route path="/Leaderboard" component={Leaderboard} />
        <Route path="/Signup" component={Signup} />
      </Routes>
    </>
  );
}

export default App;
