import { Link } from 'react-router-dom';
import Profiles from './Components/Profiles';
import './index.css';

export default function Leaderboard() {
    return (
        <>
            <h1>Are you a:</h1>
            <Link to="/Leaderboard">Player</Link>
            <Link to="/Signup">Community</Link>
        </>
    )

}