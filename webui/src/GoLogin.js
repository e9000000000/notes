import React, { useState, setState } from 'react';
import { useCookies } from 'react-cookie';

export default function GoLogin () {
	const [username, setUsername] = useState('');
	const [cookies, setCookie, removeCookie] = useCookies(['cookie-name']);

	function login() {
		var user = prompt('username', '');
		var password = prompt('password', '');
		const requestOptions = {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				username: user,
				password: password
			})
		};
		fetch('/api/users/auth/', requestOptions)
			.then(response => response.json())
			.then(data => {
				console.log(data)
				setCookie("token", data.token)
				setUsername(user);
			})
	}

	if (username == '') {
		return (
			<p onClick={login}>login</p>
		)
	} else {
		return (
			<p>{username}</p>
		)
	}
}
