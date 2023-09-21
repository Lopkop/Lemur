import React from "react";
import "../styles/App.css";
import { Footer } from "../components";

async function send_message(event) {
    // save message and send it to other user
}

export default function Chat() {
    return (
        <div className="App">
            <header>
                <h1>Chat</h1>
            </header>
            <main>
                <div className="chat">
                    <div className="send-form">
                        <input id="input-message"
                            type="text"
                            placeholder="Write message..."
                            className="message-button"/>
                    </div>
                </div>
                <button >Send message</button>
            </main>
            <Footer />
        </div>
    );
}
