import { React, useEffect, useState }  from "react";

import "../styles/App.css";
import { Footer, user_is_logged_in, createChat } from "../components";

import "bootstrap/dist/css/bootstrap.min.css";

function redirect_to_create_chat() {
       window.location.pathname = `/create_chat`;
}
function redirect_to_connect_chat() {
       window.location.pathname = `/connect_chat`;
}


function Root2_render() {
    let [user, setUser] = useState();
    useEffect(() => {
        async function fetchData() {
            const logged_in = await user_is_logged_in();
            setUser(logged_in);
            }
            fetchData();
        }, [])
    if (user) {
        return (
            <div className="App">
                <header>
                    <h1>Chat Service</h1>
                </header>
                <main>
                    <span className="some-text">The world is dual, so you have only two choices.</span>
                    <div className="auth-buttons-container">
                      <button onClick={(event) => createChat(event)} variant="secondary" className="login-button">
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
    // BUG: If i uncomment this code and user is logged in
    // you will be always (strangely) redirected to "/" and then from "/"
    // you will be redirected back here and so on ...
//     else {
//         window.location.pathname = `/`;
//     }
}

export default function Root2() {
    return (
        <section>
            {Root2_render()}
        </section>
    )
}