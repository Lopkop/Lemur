import { React, useEffect, useState }  from "react";

import "../styles/App.css";
import { user_is_logged_in, Footer, get_user } from "../components";

async function login(event) {
    event.preventDefault();
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let lifetime = 5;
    let response = await fetch("http://localhost:8000/login/", {
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
        alert("Either username or password is incorrect");
    }
}

function Login_render() {
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
                    <div className="tab-content">
                      <div className="tab-pane fade show active" id="pills-login" role="tabpanel" aria-labelledby="tab-login">
                      <form>
                          <div className="form-outline mb-4">
                            <input id="username" className="form-control" placeholder="Username"/>
                          </div>
                          <div className="form-outline mb-4">
                            <input type="password" id="password" className="form-control" placeholder="Password"/>
                          </div>
                          <button onClick={(event) => login(event)}>Login</button>
                        </form>
                      </div>
                    </div>
                </main>
                <Footer />
            </div>
    );
    }
}


export default function Login() {
     return (
        <section>
            {Login_render()}
        </section>
    )
}
