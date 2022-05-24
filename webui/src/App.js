import useCookie from 'react-use-cookie'

import './App.css'
import Header from './components/Header.js'
import Notes from './components/Notes.js'

function App() {
  const [token, setToken] = useCookie('token')

  return (
    <div className="App">
      <Header token={token} setToken={setToken} />
      <Notes token={token} setToken={setToken} />
    </div>
  );
}

export default App;
