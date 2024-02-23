import React from "react";
import "../styles/App.css";
import { Footer } from "../components";

async function connect(event) {
    let username = document.getElementById("input-username").value; // change how i get username here
    let chat = document.getElementById("chat-name").value;
    let response = await fetch("http://localhost:8000/connect-to-chat/", {
        method: 'POST',
        headers: {
        "Content-type": "application/json"
        },
        body: JSON.stringify({
        "name": `${chat}`,
        "messages": [],
        "users": [{"name": `${username}`}]
        })
    }).then(response => response.json());


    if (response.status === true) {
        localStorage.chat = chat
        localStorage.user = username
        window.location.pathname = `/chat/${chat}`;
        // todo: render new page with chat
    } else {
        alert("Either username or chatroom name is incorrect");
    }
}

export default function Chat() {
    return (
        <div className="App">
            <header>
                <h1>Chat Service</h1>
            </header>
            <main>
                <input
                    id="chat-name"
                    type="text"
                    className="connect-chat"
                    placeholder="Chatroom name"
                />
                <button onClick={(event) => connect(event)}>Connect</button>
            </main>
            <Footer />
        </div>
    );
}
