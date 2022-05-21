import React, { useState, useEffect } from 'react';
import { useCookies } from 'react-cookie';

export default function GoLogin () {
	const [username, setUsername] = useState("");
	const [cookies, setCookie, removeCookie] = useCookies(['cookie-name']);

	function login() {
		// TODO: make normal login form
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
				setCookie("token", data.token)
				request_user_data_if_have_token();
			})
	}

	function request_user_data_if_have_token() {
		fetch('/api/users/self/', {method: 'GET'})
			.then(response => {
				if (response.status == 200) {
					return response.json();
				}
			})
			.then(data => {
				setUsername(data.username);
			})
	}

	useEffect(() => {
		request_user_data_if_have_token();
	}, [])

	if (username) {
		return (
			<a to="/profile/">{username}</a>
		)
	} else {
		return (
			<a onClick={login}>login</a>
		)
	}
}
