import { React, useEffect, useState }  from "react";

import "../styles/App.css";
import { user_is_logged_in, Footer, get_user } from "../components";

async function signup(event) {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let lifetime = document.getElementById("lifetime").value;
    let response = await fetch("http://localhost:8000/sign-up/", {
        method: 'POST',
        headers: {
        "Content-type": "application/json"
        },
        body: JSON.stringify({
        "name": `${username}`,
        "password": `${password}`,
        "lifetime": `${lifetime}`
        })
    }).then(response => response.json());

    if (response.status === 201) {
        localStorage.token = response.access_token;
        window.location.pathname = `/chats`; // todo: render new page
    } else {
        alert("User with this username already exists");
    }
}

function Signup_render() {
    const [user, setUser] = useState();
    useEffect(() => {
        async function fetchData() {
            const logged_in = await user_is_logged_in();
            setUser(logged_in);
            }
            fetchData();
        }, [])
    if (user) {
        window.location.pathname = `/chats`;
    } else {
        return (
            <div className="App">
                <header>
                    <h1>Chat Service</h1>
                </header>
                <main>
                    <input
                        id="username"
                        type="text"
                        className="connect-chat"
                        placeholder="Username"
                    />
                    <input
                        id="password"
                        type="password"
                        className="connect-chat"
                        placeholder="Password"
                    />
                    <input
                        id="lifetime"
                        type="integer"
                        className="connect-chat"
                        placeholder="Lifetime"
                    />
                    <button onClick={(event) => signup(event)}>Sign Up</button>
                </main>
                <Footer />
            </div>
        );
    }
}


export default function Login() {
     return (
        <section>
            {Signup_render()}
        </section>
    )
}