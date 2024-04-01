import { React, useEffect, useState, useRef }  from "react";
import { Footer, get_user  } from "../components";
import '../styles/chat.css';

import {
Tile,
TextInput,
Button,
InlineNotification,
} from "@carbon/react";

import { onDestroy, onMount } from "react";


let messageText = "";
let senderId = "";
let messages = [];
const chatname = localStorage.getItem('chat')


export default function Chat() {
//   const [messages, setMessages] = useState([]);
//   const [newMessage, setNewMessage] = useState('');
//   const messageEndRef = useRef(null);
//   const websocketRef = useRef(null);
//       useEffect(() => {
//         const fetchMessages = async () => {
//           try {
//             const response = await fetch(`http://localhost:8000/get-messages?chatname=${chatname}`);
//             if (!response.ok) {
//               throw new Error('Failed to fetch messages');
//             }
//             const data = await response.json();
//             setMessages(data);
//           } catch (error) {
//             console.error('Error fetching messages:', error);
//           }
//         };
//         fetchMessages();
//       }, [chatname]);

  const [user, setUser] = useState(null);
  const [ws, setWs] = useState(null);
  const messagesRef = useRef(null);

  useEffect(() => {
    async function fetchData() {
      const response = await get_user();
      if (response) {
        setUser(response.name);
        const chatname = localStorage.getItem('chat');
        const websocket = new WebSocket(`ws://localhost:8000/${chatname}/${response.name}`);
        setWs(websocket);
      }
    }
    fetchData();
  }, []);

  useEffect(() => {
    if (ws) {
      ws.onmessage = function (event) {
        const data = JSON.parse(event.data);
        const newMessage = document.createElement('p');
        newMessage.textContent = `${data.user} sent ${data.text}`;
        messagesRef.current.appendChild(newMessage);
        messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
      };
    }
  }, [ws]);

  function sendMessage(event) {
    const messageInput = document.getElementById("messageInput");
    const message = messageInput.value;
    if (ws && ws.readyState === WebSocket.OPEN && message) {
      ws.send(message);
      messageInput.value = "";
    } else {
      console.error("WebSocket connection not open.");
    }
  }

    function handleKeyPress(event) {
    if (event.key === 'Enter') {
      event.preventDefault(); // Prevent default behavior of tabbing
      // Trigger the click event of the "Send" button
      document.getElementById("sendButton").click();
    }
  }

  return (
  <div>
    <div className="chat-container">
      <header className="chat-header">
        <h1>{chatname}</h1>
      </header>
      <div className="chat-messages" ref={messagesRef}></div>
      <div className="chat-input">
        <TextInput id="messageInput" labelText="Type a message" onKeyDown={handleKeyPress}/>
        <Button id="sendButton" onClick={sendMessage}>Send</Button>
      </div>
    </div>
    <Footer />
  </div>
  );
}