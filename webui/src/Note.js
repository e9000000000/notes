import React from 'react';

export default ({data}) => {
	return (
		<div className='note'>
			<p>{data.visibility}</p>
			<p>{data.text}</p>
			<p>{data.creation_date}</p>
		</div>
	)
}
