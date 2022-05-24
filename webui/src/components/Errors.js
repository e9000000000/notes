import Button from './Button.js'

const Errors = ({data, onClose}) => {
  return (
    <>
    <div className='shadowall' />
    <div className='popup'>
      <h1 className='errorsh1'>Errors</h1>
      {Object.keys(data).map((key, i) => (
        <div className='errordetails'>
          <h2>{key}</h2>
          <p>{data[key]}</p>
        </div>
      ))}
      <Button text='close' onClick={onClose}/>
    </div>
    </>
  )
}

export default Errors
