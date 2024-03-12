import { React, useEffect, useState, useRef }  from "react";
import { Footer, get_user  } from "../components";
import '../styles/chat.css'; // Import the CSS file for styling

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
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const messageEndRef = useRef(null);
  const websocketRef = useRef(null);
      useEffect(() => {
        const fetchMessages = async () => {
          try {
            const response = await fetch(`http://localhost:8000/get-messages?chatname=${chatname}`);
            if (!response.ok) {
              throw new Error('Failed to fetch messages');
            }
            const data = await response.json();
            setMessages(data);
            scrollToBottom();
          } catch (error) {
            console.error('Error fetching messages:', error);
          }
        };

        fetchMessages();
      }, [chatname]);
  const [user, setUser] = useState([]);
  useEffect(() => {
  const get_u = async () => {
            let user = await get_user();
        }
    setUser(get_u())
    console.log(user, 'FAFADFA')
    websocketRef.current = new WebSocket(`ws://localhost:8000/${chatname}/a`);

    websocketRef.current.onopen = () => {
      console.log('Connected to websocket server');
    };

    websocketRef.current.onclose = () => {
      console.log('Disconnected from websocket server');
    };

    websocketRef.current.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages((prevMessages) => [...prevMessages, message]);
      scrollToBottom();
    };

    return () => {
      if (websocketRef.current) {
        websocketRef.current.close();
      }
    };
  }, []);

  const scrollToBottom = () => {
    if (messageEndRef.current) {
      messageEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleMessageChange = (event) => {
    setNewMessage(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (newMessage.trim() === '') return;
    const newMessageObj = newMessage.trim();
    websocketRef.current.send(JSON.stringify(newMessageObj));
    setNewMessage('');
    scrollToBottom(); // Scroll to bottom when a new message is sent
  };

  return (
    <div className="message-container">
      <ul className="message-list">
        {messages.map((message, index) => (
          <li key={index} className={`message-item ${message.user === 'me' ? 'me' : 'other'}`}>
            <div className="message-content">
              <span className="message-text">{message.text}</span>
            </div>
          </li>
        ))}
        <div ref={messageEndRef} />
      </ul>
      <form className="message-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          className="message-input"
          placeholder="Type your message..."
          value={newMessage}
          onChange={handleMessageChange}
        />
        <Button type="submit">
          Send
        </Button>
      </form>
    </div>
  );
}