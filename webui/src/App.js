import { useState } from 'react'
import useCookie from 'react-use-cookie'
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from 'react-router-dom';

import './App.css'
import Header from './components/Header.js'
import Notes from './components/Notes.js'
import NoteDetails from './components/NoteDetails.js'

function App() {
  const [token, setToken] = useCookie('token')
  const [user, setUser] = useState(null)

  return (
    <Router>
      <div className="App">
        <Header token={token} setToken={setToken} user={user} setUser={setUser} />
        <Routes>
          <Route path='/' element={<Notes token={token} user={user} />} />
          <Route path='/:id' element={<NoteDetails token={token} user={user} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
