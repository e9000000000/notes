import { useState, useEffect } from 'react'

import { baseUrl } from '../config.js'
import Button from './Button.js'
import Input from './Input.js'
import Errors from './Errors.js'

const AddNote = ({onClose, token, notes, setNotes}) => {
  const [text, setText] = useState('')
  const [isPublic, setIsPublic] = useState(false)
  const [errors, setErrors] = useState(null)
  const [showErrors, setShowErrors] = useState(false)

  const create = () => {
    var requestOpts = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + token
      },
      body: JSON.stringify({
        'text': text,
        'visibility': isPublic ? 'BY_URL' : 'PRIVATE'
      })
    }
    fetch(baseUrl + "/api/notes/", requestOpts)
      .then(resp => {
        if (!resp.ok)
          resp.json().then(data => {
            setErrors(data)
          })
        else
          resp.json().then(data => {
            if (notes)
              setNotes([data].concat(notes))
            else
              setNotes([data])
            onClose()
          })
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
      <h1>Add note</h1>
      <Input type='textarea' placeholder='text' value={text} onChange={(e) => setText(e.target.value)} />
      <Button text={isPublic ? 'awailable by url' : 'private'} onClick={() => setIsPublic(!isPublic)}/>
      <div className='row'>
        <Button text='close' onClick={onClose}/>
        <Button text='add' onClick={create}/>
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

export default AddNote
