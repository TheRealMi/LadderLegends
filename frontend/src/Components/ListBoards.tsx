function ListBoards() {
  const boards = [
    "NLG Summer Gaming",
    "RoK Esports Fall Ladder",
    "Metashift League Ladder",
  ];
  return (
    <div>
      <h1>List of Leaderboards</h1>
      <ul className="list-group">
        {boards.map((board) => (
          <li key={board} className="list-group-item">
            {board}
          </li>
        ))}
      </ul>
    </div>
  );
}
export default ListBoards;
