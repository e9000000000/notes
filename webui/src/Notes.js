import React, {useState} from 'react';
import Note from './Note';

export default () => {
	const [notes, setNotes] = useState([
		{id: 'feewffe-few-fw-effe', text: 'weffewfwf', creation_date: '12 15'},
		{id: 'fewffeb-few-fw-effe', text: 'effeefef', creation_date: '11 50'},
		{id: 'aaaaaaa-few-fw-effe', text: 'fewefwewf', creation_date: '3 14'}
	])

	return (
		<div className='notes'>
			{notes.map(data => {
				return (
					<Note data={data} key={data.id} />
				)
			})}
		</div>
	)
}
