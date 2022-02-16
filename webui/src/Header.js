import React, { useState } from 'react';
import GoLogin from './GoLogin';

export default function Header() {
	return (
		<header>
			<h1>Notes</h1>
			<GoLogin />
		</header>
	);
}
