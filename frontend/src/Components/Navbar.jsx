import { Link } from "react-router-dom";
function Navbar() {
  return (
    <nav class="headerNav">
      <Link to="/" class="site-title">
        Ladder League
      </Link>
      <ul>
        <CustomLink href="/Components/ListBoards">Leaderboard</CustomLink>
        <CustomLink href="/Signup">Sign up</CustomLink>
      </ul>
    </nav>
  );
}

function CustomLink({ href, children, ...props }) {
  return (
    <li>
      <a href={href}>{children}</a>
    </li>
  );
}
export default Navbar;
