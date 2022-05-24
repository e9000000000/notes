import { useNavigate } from 'react-router-dom';

import Button from './Button.js'

const Note = ({ data }) => {
  const navigate = useNavigate()

  return (
    <div className='note'>
        <h2>{data.visibility === 'PRIVATE' ? 'Private' : 'Awailable by url'}</h2>
      <Button text='open' onClick={() => navigate('/' + data.id)} />
      <p>{data.text}</p>
    </div>
  )
}

export default Note
