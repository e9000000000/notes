import { useState, useEffect } from 'react'

import { baseUrl } from '../config.js'
import Button from './Button.js'
import Input from './Input.js'
import Errors from './Errors.js'

const Registration = ({onClose}) => {

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [captcha, setCaptcha] = useState(null)
  const [changeCaptcha, setChangeCaptcha] = useState(0)
  const [captchaValue, setCaptchaValue] = useState(null)
  const [errors, setErrors] = useState(null)
  const [showErrors, setShowErrors] = useState(false)

  const register = () => {
    var requestOpts = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json'},
      body: JSON.stringify({
        'captcha_key': captcha.captcha_key,
        'captcha_value': captchaValue,
        'username': username,
        'password': password
      })
    }
    fetch(baseUrl + '/api/users/register/', requestOpts)
      .then((resp) => {
        if (resp.status !== 204)
          return resp.json()
        else
          onClose()
        return {success: 1}
      })
      .then((data) => {
        if (data.success === 1)
          return

        setErrors(data)
      })
  }

  useEffect(() => {
    if (errors === null)
      return
    setShowErrors(true)
  }, [errors])

  useEffect(() => {
    var requestOpts = {
      method: 'POST'
    }
    fetch(baseUrl + '/api/captcha/', requestOpts)
      .then((resp) => resp.json())
      .then((data) => {
        setCaptcha(data)
      })
  }, [changeCaptcha])

  return (
    <>
    <div className='shadowall' />
    <div className='popup'>
      <h1>Registration</h1>
      <Input placeholder='username' value={username} onChange={(e) => setUsername(e.target.value)} />
      <Input placeholder='password' value={password} onChange={(e) => setPassword(e.target.value)} />
      {captcha === null ? (
        <p>captcha loading...</p>
      ) : (
        <img alt='captcha, solve it' src={`data:${captcha.image_type};${captcha.image_decode},${captcha.captcha_image}`} />
      )}
      <Input placeholder='captcha value' value={captchaValue} onChange={(e) => setCaptchaValue(e.target.value)} />
      <Button text='change captcha' onClick={() => setChangeCaptcha(changeCaptcha + 1)}/>
      <div className='row'>
        <Button text='close' onClick={onClose}/>
        <Button text='register' onClick={register}/>
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

export default Registration
