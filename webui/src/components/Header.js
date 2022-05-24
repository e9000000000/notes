import { useState, useEffect } from 'react'
import useCookie from 'react-use-cookie'

import { baseUrl } from '../config.js'
import Button from './Button.js'
import Registration from './Registration.js'
import Login from './Login.js'

const Header = ({title}) => {
  const [token, setToken] = useCookie('token')

  const [user, setUser] = useState(null)
  const [showRegistration, setShowRegistration] = useState(false)
  const [showLogin, setShowLogin] = useState(false)

  const logout = () => {
    const requestOpts = {
      method: 'DELETE',
      headers: { 'Authorization': 'Token ' + token}
    }
    fetch(baseUrl + "/api/users/unauth/", requestOpts)
      .then(resp => {
        if (resp.status === 204) {
          setToken('0')
        } else {
          alert('cant delete token for unknown reason')
        }
      })
  }

  useEffect(() => {
    if (!token || token === '0') {
      setUser(null)
      return
    }

    const requestOpts = {
      method: 'GET',
      headers: { 'Authorization': 'Token ' + token}
    }
    fetch(baseUrl + '/api/users/self/', requestOpts)
      .then(resp => resp.json())
      .then(data => setUser(data))
  }, [token])

  return (
    <header className='header'>
      <div className='headerDiv'>
        <h1>{title}</h1>
      </div>
      <div className='headerDiv'>
        {user == null ? (
          <>
            <Button text='register' onClick={() => setShowRegistration(true)} />
            <Button text='login' onClick={() => setShowLogin(true)} />
          </>
        ) : (
          <>
            <Button text={user.username} />
            <Button text='logout' onClick={logout} />
          </>
        )}
      </div>
      {showLogin ? (
        <Login setToken={setToken} onClose={() => setShowLogin(false)}/>
      ) : (
        null
      )}
      {showRegistration ? (
        <Registration onClose={() => setShowRegistration(false)}/>
      ) : (
        null
      )}
    </header>
  )
}

export default Header