import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

import { baseUrl } from '../config.js'
import Button from './Button.js'
import Input from './Input.js'
import Errors from './Errors.js'

const EditNote = ({onClose, token, note, setNote}) => {
  let { id } = useParams()

  const [text, setText] = useState(note.text)
  const [isPublic, setIsPublic] = useState(note.visibility === 'PRIVATE' ? false : true)
  const [errors, setErrors] = useState(null)
  const [showErrors, setShowErrors] = useState(false)

  const update = () => {
    var requestOpts = {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + token
      },
      body: JSON.stringify({
        'text': text,
        'visibility': isPublic ? 'BY_URL' : 'PRIVATE'
      })
    }
    fetch(baseUrl + `/api/notes/${id}/`, requestOpts)
      .then(resp => {
        if (resp.ok)
          resp.json().then(data => {
            setNote(data)
            onClose()
          })
        else
          resp.json().then(data => {
            setErrors(data)
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
      <h1>Edit note</h1>
      <Input type='textarea' placeholder='text' value={text} onChange={(e) => setText(e.target.value)} />
      <Button text={isPublic ? 'awailable by url' : 'private'} onClick={() => setIsPublic(!isPublic)}/>
      <div className='row'>
        <Button text='close' onClick={onClose}/>
        <Button text='update' onClick={update}/>
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

export default EditNote
