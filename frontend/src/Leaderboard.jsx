import {useState} from 'react'
import Profiles from './Components/Profiles';
import './index.css';
export default function Leaderboard(){

   
    const [leaderboard, setLeaderboard] = useState([{name:"Angel"}, {name:"Mia"}, {name:"Juan"}])
    
    useEffect(() => {
        // Define the URL for your GET request
        const apiUrl = 'https://api.example.com/data';
    
        // Use the fetch API to make the GET request
        fetch(apiUrl)
          .then((response) => response.json())
          .then((result) => {
            setData(result); // Set the data in state
            setLoading(false); // Set loading to false
          })
          .catch((error) => {
            console.error('Error fetching data:', error);
            setLoading(false); 
        });
    }, []); 

    return(
        <div class="board">
            <h1 class="leaderboard">Leaderboard</h1>
            {leaderboard.map(singleLeaderboard => {
                return <h4>{singleLeaderboard.name}</h4>
            })}

            <Profiles></Profiles>    
        </div>
    )
    
}
