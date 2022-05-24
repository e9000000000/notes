import { useState, useEffect } from 'react'

import { baseUrl } from '../config.js'
import Button from './Button.js'
import Input from './Input.js'
import Errors from './Errors.js'

const Login = ({onClose, setToken}) => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [errors, setErrors] = useState(null)
  const [showErrors, setShowErrors] = useState(false)

  const login = () => {
    var requestOpts = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json'},
      body: JSON.stringify({
        'username': username,
        'password': password
      })
    }
    fetch(baseUrl + "/api/users/auth/", requestOpts)
      .then(resp => {
        if (resp.ok)
          resp.json().then(data => {
            setToken(data.token)
            onClose()
          })
        else
          resp.json().then(data => setErrors(data))
      })
  }

  useEffect(() => {
    if (errors === null)
      return
    setShowErrors(true)
  }, [errors])

  return (
    <>
    <div className='shadowall' />
    <div className='popup'>
      <h1>Login</h1>
      <Input placeholder='username' value={username} onChange={(e) => setUsername(e.target.value)} />
      <Input type='password' placeholder='password' value={password} onChange={(e) => setPassword(e.target.value)} />
      <div className='row'>
        <Button text='close' onClick={onClose}/>
        <Button text='login' onClick={login}/>
      </div>
    </div>
    {showErrors ? (
      <Errors data={errors} onClose={() => setShowErrors(false)} />
    ) : (
      null
    )}
    </>
  )
}

export default Login
