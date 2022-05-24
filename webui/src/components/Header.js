import { useState, useEffect } from 'react'
import { baseUrl } from '../config.js'
import useCookie from 'react-use-cookie'
import Button from './Button.js'

const Header = ({title}) => {
  const [user, setUser] = useState(null)

  const [token, setToken] = useCookie('token')

  const register = () => {
    // TODO: create registration popup
  }

  const login = () => {
    var username = prompt("username")
    var password = prompt("password")
    const requestOpts = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json'},
      body: JSON.stringify({
        'username': username,
        'password': password
      })
    }
    fetch(baseUrl + "/api/users/auth/", requestOpts)
      .then(resp => {
        if (resp.status === 200) {
          return resp.json()
        } else {
          alert('wrong username or password')
        }
      })
      .then(data => setToken(data.token))
  }

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
            <Button text='register' onClick={register} />
            <Button text='login' onClick={login} />
          </>
        ) : (
          <>
            <Button text={user.username} />
            <Button text='logout' onClick={logout} />
          </>
        )}
      </div>
    </header>
  )
}

export default Header
