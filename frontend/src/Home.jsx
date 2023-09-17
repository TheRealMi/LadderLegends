import { Link } from 'react-router-dom';
import Profiles from './Components/Profiles';
import './index.css';

export default function Leaderboard() {
    return (
        <>
            <div>
            <h1 class="question">Are you a:</h1>
            <Link to="/Components/Listboards"><button type="button" class="btn btn-primary mx-center p-2 " >Player</button></Link>
            <Link to="/Signup"><button type="button" class="btn btn-primary mx-center p-2" >Community</button></Link> 
            </div>
          
        </>
    )

}