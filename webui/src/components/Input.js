const Input = ({type, placeholder, value, onChange}) => {
  return (
    <>
      {type === 'text' || type === 'password' ? (
        <input className='input' type={type} placeholder={placeholder} value={value} onChange={onChange} />
      ) : type === 'textarea' ? (
        <textarea className='input' placeholder={placeholder} value={value} onChange={onChange}/>
      ) : 
      (
        <h2>wrong type</h2>
      )}
    </>
  )
}

Input.defaultProps = {    
  type: "text",    
}

export default Input
