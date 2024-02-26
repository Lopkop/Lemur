import React from "react";
import "../styles/App.css";
import { Footer } from "../components";

import "bootstrap/dist/css/bootstrap.min.css";

function redirect_to_signup() {
       window.location.pathname = `/signup`;
}
function redirect_to_login() {
       window.location.pathname = `/login`;
}

export default function Root() {
    return (
        <div className="App">
            <header>
                <h1>Chat Service</h1>
            </header>
            <main>
                <span className="some-text">The world is dual, so you have only two choices.</span>
                <div className="auth-buttons-container">
                  <button onClick={redirect_to_login} variant="secondary" className="login-button">
                    Login
                  </button>
                  <button onClick={redirect_to_signup} variant="secondary" className="signup-button">
                    Sign Up
                  </button>
                </div>
            </main>
            <Footer />
        </div>
    );
}