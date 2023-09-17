import { Link } from 'react-router-dom';
import Profiles from './Components/Profiles';
import './index.css';

export default function Leaderboard() {
    return (
        <>
        <div class="d-flex align-items-center justify-content-center">
        <div class="p-5  m-5 bg-info text-white shadow rounded-2">
            <div class="mx-auto">
            <h1 class="mx-auto">Are you a:</h1>
            </div>
            <Link to="/Components/Listboards"><button type="button" class="btn btn-primary mx-3 p-2 " >Player</button></Link>
            <Link to="/Signup"><button type="button" class="btn btn-primary mx-3 p-2" >Community</button></Link> 
            </div>
          </div>
        </>
    )

}