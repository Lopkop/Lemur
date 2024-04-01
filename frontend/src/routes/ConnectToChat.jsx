import React from "react";
import "../styles/App.css";
import { Footer, get_user } from "../components";

async function connect(event) {
    let chat = document.getElementById("chat-name").value;
    let user = await get_user()

    let response = await fetch("http://localhost:8000/connect-to-chat/", {
        method: 'POST',
        headers: {
        "Content-type": "application/json"
        },
        credentials: 'include',
        body: JSON.stringify({
        "chatname": `${chat}`,
        "username": `${user.name}`
        })
    }).then(response => response.json());
    console.log(response)
    if (response.status == 200) {
        localStorage.chat = chat
        window.location.pathname = `/chat/${chat}`;
    } else {
        alert("Chatroom name is incorrect");
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
