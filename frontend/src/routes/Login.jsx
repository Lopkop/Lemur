import React from "react";
import "../styles/App.css";
import { Footer } from "../components";

async function login() {
    console.log("hahah")
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let response = await fetch("http://localhost:8000/login/", {
        method: 'POST',
        headers: {
        "Content-type": "application/json"
        },
        body: JSON.stringify({
        "name": `${username}`,
        "password": `${password}`
        })
    }).then(response => response.json());


    if (response.status === true) {
        console.log(response)
        localStorage.user = username
        window.location.pathname = ``;
        // todo: render new page
    } else {
        alert("Either username or chatroom name is incorrect");
    }
}

export default function Login() {
    return (
        <div className="App">
            <header>
                <h1>Chat Service</h1>
            </header>
            <main>

                <div class="tab-content">
                  <div class="tab-pane fade show active" id="pills-login" role="tabpanel" aria-labelledby="tab-login">
                  <form>
                      <div class="form-outline mb-4">
                        <input id="username" class="form-control" placeholder="Username"/>
                      </div>
                      <div class="form-outline mb-4">
                        <input type="password" id="password" class="form-control" placeholder="Password"/>
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
