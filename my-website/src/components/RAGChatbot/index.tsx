'use client';

import { useState } from 'react';

export default function AIAssistantFloat() {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([
    { type: 'bot', text: 'Hi! How can I help you today?' }
  ]);

  const handleSend = () => {
    if (!message.trim()) return;
    
    setMessages([...messages, { type: 'user', text: message }]);
    setMessage('');
    
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        type: 'bot', 
        text: 'Thanks for your message! Our team will get back to you shortly.' 
      }]);
    }, 1000);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <>
      <style jsx>{`
        .ai-float-container {
          position: fixed;
          bottom: 40px;
          right: 24px;
          z-index: 50;
        }

        .ai-float-button {
          position: relative;
          width: 64px;
          height: 64px;
          background: linear-gradient(135deg, #2563eb, #9333ea);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: all 0.3s ease;
          border: 2px solid white;
          box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        }

        .ai-float-button:hover {
          transform: scale(1.1);
          box-shadow: 0 15px 35px rgba(37, 99, 235, 0.3);
        }

        .ai-float-button svg {
          width: 32px;
          height: 32px;
          color: white;
        }

        .pulse-ring {
          position: absolute;
          inset: 0;
          width: 64px;
          height: 64px;
          background: #3b82f6;
          border-radius: 50%;
          animation: ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;
          opacity: 0.2;
        }

        .online-indicator {
          position: absolute;
          top: -4px;
          right: -4px;
          width: 20px;
          height: 20px;
          background: #22c55e;
          border-radius: 50%;
          border: 2px solid white;
        }

        @keyframes ping {
          75%, 100% {
            transform: scale(1.5);
            opacity: 0;
          }
        }

        .chat-window {
          position: fixed;
          bottom: 128px;
          right: 24px;
          width: 370px;
          height: 400px;
          background: white;
          border-radius: 16px;
          box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
          z-index: 50;
          display: flex;
          flex-direction: column;
          overflow: hidden;
          border: 1px solid #e5e7eb;
        }

        .chat-header {
          background: linear-gradient(135deg, #2563eb, #9333ea);
          color: white;
          padding: 16px;
          display: flex;
          align-items: center;
          justify-content: space-between;
        }

        .chat-header-left {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .chat-avatar {
          width: 40px;
          height: 40px;
          background: rgba(255, 255, 255, 0.2);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .chat-avatar svg {
          width: 24px;
          height: 24px;
        }

        .chat-title h3 {
          font-size: 16px;
          font-weight: 600;
          margin: 0;
        }

        .chat-title p {
          font-size: 12px;
          opacity: 0.8;
          margin: 0;
        }

        .close-btn {
          background: none;
          border: none;
          color: white;
          cursor: pointer;
          padding: 4px;
          border-radius: 8px;
          transition: background 0.2s;
        }

        .close-btn:hover {
          background: rgba(255, 255, 255, 0.2);
        }

        .close-btn svg {
          width: 20px;
          height: 20px;
        }

        .chat-messages {
          flex: 1;
          overflow-y: auto;
          padding: 16px;
          background: #f9fafb;
          display: flex;
          flex-direction: column;
          gap: 16px;
        }

        .message {
          display: flex;
        }

        .message.user {
          justify-content: flex-end;
        }

        .message.bot {
          justify-content: flex-start;
        }

        .message-bubble {
          max-width: 80%;
          padding: 12px 16px;
          border-radius: 16px;
          word-wrap: break-word;
        }

        .message.user .message-bubble {
          background: #2563eb;
          color: white;
          border-bottom-right-radius: 4px;
        }

        .message.bot .message-bubble {
          background: white;
          color: #1f2937;
          border-bottom-left-radius: 4px;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .chat-input {
          padding: 16px;
          background: white;
          border-top: 1px solid #e5e7eb;
          display: flex;
          gap: 8px;
        }

        .chat-input input {
          flex: 1;
          padding: 10px 16px;
          border: 1px solid #d1d5db;
          border-radius: 24px;
          outline: none;
          font-size: 14px;
          font-family: inherit;
        }

        .chat-input input:focus {
          border-color: #2563eb;
          box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }

        .send-btn {
          width: 40px;
          height: 40px;
          background: linear-gradient(135deg, #2563eb, #9333ea);
          border: none;
          border-radius: 50%;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.3s;
        }

        .send-btn:hover {
          transform: scale(1.05);
          box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
        }

        .send-btn svg {
          width: 20px;
          height: 20px;
          color: white;
        }
      `}</style>

      {/* Chat Window */}
      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <div className="chat-header-left">
              <div className="chat-avatar">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
                </svg>
              </div>
              <div className="chat-title">
                <h3>AI Assistant</h3>
                <p>Online now</p>
              </div>
            </div>
            <button className="close-btn" onClick={() => setIsOpen(false)}>
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <div className="chat-messages">
            {messages.map((msg, i) => (
              <div key={i} className={`message ${msg.type}`}>
                <div className="message-bubble">{msg.text}</div>
              </div>
            ))}
          </div>

          <div className="chat-input">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
            />
            <button className="send-btn" onClick={handleSend}>
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
              </svg>
            </button>
          </div>
        </div>
      )}

      {/* Float Button */}
      <div className="ai-float-container">
        <div className="ai-float-button" onClick={() => setIsOpen(!isOpen)}>
          <div className="pulse-ring"></div>
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
          </svg>
          <div className="online-indicator"></div>
        </div>
      </div>
    </>
  );
}