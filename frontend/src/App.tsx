import React from 'react';
import './styles/App.css' 

// todo: finish footer
function App() {
  return (
    <div className="App">
    	<header>
    		<h1>Chat Service</h1>
    	</header>
    	<main>
		<input id="input-username" type="text" placeholder="Write username"/>
	</main>

	<footer>
		<a href="#">about us</a>
		discord icon
	</footer>
    </div>
  );
}

export default App;
