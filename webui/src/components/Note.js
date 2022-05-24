import Button from './Button.js'

const Note = ({ data }) => {
  return (
    <div className='note'>
      <p>{data.text}</p>
      <div>
        <Button text='open' />
        <Button text='edit' />
        <Button text='remove' />
        <Button text={data.visibility === 'PRIVATE' ? 'make public' : 'make private'} />
      </div>
    </div>
  )
}

export default Note
