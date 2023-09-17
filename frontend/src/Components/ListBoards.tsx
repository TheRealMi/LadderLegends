import { useState } from "react";
import React from "react";
import Leaderboard from "../Leaderboard";
import { Route, Routes, Link } from "react-router-dom";

function ListBoards() {
  let boards = [
    "NLG Summer Gaming",
    "RoK Esports Fall Ladder",
    "Metashift League Ladder",
  ];
  const [selectedIndex, setSelectedIndex] = useState(-1);

  return (
    <div>
      <h1>List of Leaderboards</h1>
      {boards.length === 0 && (
        <p>Looks like your leaderboards are at another Nexus</p>
      )}
      <ul className="list-group">
        {boards.map((board, index) => (
          <li
            key={board}
            className={
              selectedIndex === index
                ? "list-group-item active list-group-item-primary"
                : "list-group-item"
            }
            onClick={() => {
              setSelectedIndex(index);
              console.log(board);
            }}
          >
            {board}
          </li>
        ))}
      </ul>
    </div>
  );
}
export default ListBoards;
