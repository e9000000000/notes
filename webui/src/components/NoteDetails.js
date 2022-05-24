import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'

import { baseUrl } from '../config.js'
import Button from './Button.js'
import Errors from './Errors.js'
import EditNote from './EditNote.js'

const NoteDetails = ({ token, user }) => {
  let { id } = useParams()
  const navigate = useNavigate()

  const [note, setNote] = useState(null)
  const [errors, setErrors] = useState(null)
  const [showErrors, setShowErrors] = useState(false)
  const [showEdit, setShowEdit] = useState(false)

  const remove = () => {
    const requestOpts = {
      method: 'DELETE',
      headers: { 'Authorization': 'Token ' + token}
    }
    fetch(baseUrl + `/api/notes/${id}/`, requestOpts)
      .then(resp => {
        if (resp.ok)
          navigate('/')
        else
          resp.json().then(data => setErrors(data))
      })
  }

  useEffect(() => {
    const requestOpts = {
      method: 'GET',
      headers: { 'Authorization': 'Token ' + token}
    }

    if (!user) {
      requestOpts.headers = {}
    }

    fetch(`${baseUrl}/api/notes/${id}/`, requestOpts)
      .then(resp => {
        if (resp.ok)
          resp.json().then(data => setNote(data))
        else
          setNote(null)
      })
  }, [token, id])

  useEffect(() => {
    if (errors === null)
      return
    setShowErrors(true)
  }, [errors])

  return (
    <>
      <div className='notes-container'>
        <div className='notes'>
          {note ? (
            <>
              <Button text='back' onClick={() => navigate('/')} />
              <div className='note-detail'>
                <div>
                  <h2>{note.visibility === 'PRIVATE' ? 'Private' : 'Awailable by url'}</h2>
                  <p>{note.text}</p>
                </div>
                { user && note.author === user.id ? (
                <div>
                  <Button text='edit' onClick={() => setShowEdit(true)} />
                  <Button text='delete' onClick={remove} />
                </div>
                ) : (
                  null
                )}
              </div>
            </>
          ) : (
            <h2>404, no notes</h2>
          )}
        </div>
      </div>
      {showErrors ? (
        <Errors data={errors} onClose={() => setShowErrors(false)} />
      ) : (
        null
      )}
      {showEdit ? (
        <EditNote token={token} note={note} setNote={setNote} onClose={() => setShowEdit(false)} />
      ) : (
        null
      )}
    </>
  )
}

export default NoteDetails
