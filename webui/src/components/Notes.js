import { useState, useEffect } from 'react'

import { baseUrl } from '../config.js'
import Button from './Button.js'
import Note from './Note.js'
import AddNote from './AddNote.js'

const Notes = ({ token, user }) => {
  const [notes, setNotes] = useState(null)
  const [addShow, setAddShow] = useState(false)



  useEffect(() => {
    if (addShow)
      return
    if (!token || token === '0') {
      setNotes(null)
      return
    }

    const requestOpts = {
      method: 'GET',
      headers: { 'Authorization': 'Token ' + token}
    }
    fetch(baseUrl + '/api/notes/', requestOpts)
      .then(resp => {
        if (resp.ok)
          resp.json().then(data => setNotes(data))
        else
          setNotes(null)
      })
      
  }, [token, addShow])

  return (
    <div className='notes-container'>
      { user ? (
        <Button text='new note' onClick={() => setAddShow(true)} />
      ) : (
        null
      )}
      <div className='notes'>
        {notes ? notes.map((note, i) => (
          <Note key={note.id} data={note} />
        )) : (
          <h2>no notes</h2>
        )}
      </div>
      {addShow ? (
        <AddNote notes={notes} setNotes={setNotes} token={token} onClose={() => setAddShow(false)} />
      ) : (
        null
      )}
    </div>
  )
}

export default Notes
