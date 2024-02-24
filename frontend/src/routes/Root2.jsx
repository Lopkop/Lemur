import React from "react";
import "../styles/App.css";
import { Footer } from "../components";

import "bootstrap/dist/css/bootstrap.min.css";

function redirect_to_create_chat() {
       window.location.pathname = `/create_chat`;
}
function redirect_to_connect_chat() {
       window.location.pathname = `/connect_chat`;
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
                  <button onClick={redirect_to_create_chat} variant="secondary" className="login-button">
                    Create chat
                  </button>
                  <button onClick={redirect_to_connect_chat} variant="secondary" className="signup-button">
                    Connect to chat
                  </button>
                </div>
            </main>
            <Footer />
        </div>
    );
}
