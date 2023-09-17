import React from 'react';
import Navbar from './Components/Navbar';
import Leaderboard from './Leaderboard';
import Signup from './Signup';
import './index.css'
import {Route, Routes} from "react-router-dom"


function App() {

  return (
    <>
      <React.Fragment>
          <Navbar/>
          
      </React.Fragment>
      <div class="container"></div>
      <Routes>
        
        <Route path="/Leaderboard" element={<Leaderboard />} />
        <Route path="/Signup" element={<Signup />} />
      
      </Routes>
    </>
  )
}

export default App
