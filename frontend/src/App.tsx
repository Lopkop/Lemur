import React from 'react';
import './styles/App.css' 
import {Footer} from './components'

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
	<Footer />
    </div>
  );
}

export default App;
