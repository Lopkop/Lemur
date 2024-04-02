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
      else {
         window.location.pathname = `/`;
      }
    }
    fetchData();
  }, []);

  useEffect(() => {
    if (ws) {
      ws.onmessage = function (event) {
        const data = JSON.parse(event.data);
        let node = document.getElementById('messageContainer');
        node.insertAdjacentHTML('beforeend', `        <div>
          <div><strong>${data.user}</strong> (${data.created_at}):</div>
          <div>${data.text}</div>
        </div>`);
        messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
      };
    }
  }, [ws]);

    const [messages, setMessages] = useState([]);
      useEffect(() => {
        const fetchMessages = async () => {
          try {
            const response = await fetch(`http://localhost:8000/get-messages/${chatname}`, {
            method: 'GET',
            credentials: 'include'
            })

            const data = await response.json();
            setMessages(data);
          } catch (error) {
            console.error('Error fetching messages:', error);
          }
        };
        fetchMessages();
      }, [chatname]);

    function Message({ user, text, created_at }) {
      return (
        <div>
          <div><strong>{user}</strong> ({created_at}):</div>
          <div>{text}</div>
        </div>
      );
    }




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
      event.preventDefault();
      document.getElementById("sendButton").click();
    }
  }

    function copyText() {
      var textToCopy = document.getElementById('copyText').textContent;
      navigator.clipboard.writeText(textToCopy).then(function() {
      }, function(err) {
        console.error('Unable to copy text: ', err);
      });
    }

    function MessageList({ messages }) {
      return (
        <div>
          {messages.map((message, index) => (
            <Message key={index} {...message} />
          ))}
        </div>
      );
    }
  return (
  <div>
    <div className="chat-container">
      <header className="chat-header">
        <div className="container" id="container">
          <h1 onClick={copyText} className="chat-name" id="copyText">{chatname}</h1>
        </div>
      </header>
      <div className="chat-messages" id="messageContainer" ref={messagesRef}>
      <MessageList messages={messages} />
      </div>
      <div className="chat-input">
        <input id="messageInput" placeholder="Type a message" onKeyDown={handleKeyPress}/>
        <Button id="sendButton" onClick={sendMessage}>Send</Button>
      </div>
    </div>
    <Footer />
  </div>
  );
}