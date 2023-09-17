import { useState } from "react";
import React from "react";
import Leaderboard from "../Leaderboard";
import { Link } from "react-router-dom";

  function ListBoards() {
    let boards = [
      "NLG Summer Gaming",
      "RoK Esports Fall Ladder",
      "Metashift League Ladder",
    ];
    const [selectedIndex, setSelectedIndex] = useState(-1);

    return (
      <div>
        <div className="mx-auto">
          <h1 className="mx-auto">Leaderboard</h1>
        </div>
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
             <Link to="/Leaderboard">{board}</Link>
            </li>
          ))}
        </ul>
      </div>
    );
  }
  export default ListBoards;
