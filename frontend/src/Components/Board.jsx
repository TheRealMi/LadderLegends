import Profiles from './Profiles';
import '../index.css';
function Board(){
    return(
        <div class="board">
            <h1 class="leaderboard">Leaderboard</h1>

            <Profiles></Profiles>    
        </div>
    )

}

export default Board;