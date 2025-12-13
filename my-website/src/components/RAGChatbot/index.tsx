import React, { useState, useRef, useEffect } from 'react';

interface Message {
  type: 'user' | 'bot';
  text: string;
  sources?: Array<{ title: string; relevance_score: number }>;
  timestamp: Date;
}

export default function AIAssistantFloat() {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    { 
      type: 'bot', 
      text: 'Hi! I\'m your Physical AI & Humanoid Robotics assistant. Ask me anything about robotics, AI, ROS 2, humanoid design, or locomotion!',
      timestamp: new Date()
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

const BACKEND_URL = 'https://muhammadjibran-mjr.hf.space/api/predict';


  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!message.trim() || isLoading) return;

    const userMessage = message.trim();
    setMessage('');

    setMessages(prev => [...prev, { type: 'user', text: userMessage, timestamp: new Date() }]);
    setIsLoading(true);

    try {
      const response = await fetch(BACKEND_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: [userMessage] }),
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();

      const botMessage: Message = {
        type: 'bot',
        text: data.data[0][0],
        sources: data.data[0][1],
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, {
        type: 'bot',
        text: 'I apologize, but I cannot reach the server. Please try again later.',
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const formatTime = (date: Date) =>
    date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });

  return (
    <div>
    <>
      <style>{`
        .ai-float-container {
          position: fixed;
          bottom: 40px;
          right: 24px;
          z-index: 9999;
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
          animation: pulse-dot 2s ease-in-out infinite;
        }

        @keyframes ping {
          75%, 100% {
            transform: scale(1.5);
            opacity: 0;
          }
        }

        @keyframes pulse-dot {
          0%, 100% {
            opacity: 1;
          }
          50% {
            opacity: 0.5;
          }
        }

        .chat-window {
          position: fixed;
          bottom: 128px;
          right: 24px;
          width: 420px;
          max-width: calc(100vw - 48px);
          height: 550px;
          max-height: calc(100vh - 200px);
          background: white;
          border-radius: 16px;
          box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
          z-index: 9999;
          display: flex;
          flex-direction: column;
          overflow: hidden;
          border: 1px solid #e5e7eb;
          animation: slideUp 0.3s ease-out;
        }

        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
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
          opacity: 0.9;
          margin: 0;
          margin-top: 2px;
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

        .chat-messages::-webkit-scrollbar {
          width: 6px;
        }

        .chat-messages::-webkit-scrollbar-track {
          background: #f1f1f1;
        }

        .chat-messages::-webkit-scrollbar-thumb {
          background: #cbd5e1;
          border-radius: 3px;
        }

        .chat-messages::-webkit-scrollbar-thumb:hover {
          background: #94a3b8;
        }

        .message {
          display: flex;
          flex-direction: column;
          animation: fadeIn 0.3s ease-out;
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .message.user {
          align-items: flex-end;
        }

        .message.bot {
          align-items: flex-start;
        }

        .message-bubble {
          max-width: 85%;
          padding: 12px 16px;
          border-radius: 16px;
          word-wrap: break-word;
          line-height: 1.5;
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

        .message-time {
          font-size: 11px;
          color: #9ca3af;
          margin-top: 4px;
          padding: 0 4px;
        }

        .sources {
          margin-top: 8px;
          padding: 8px;
          background: #f3f4f6;
          border-radius: 8px;
          font-size: 12px;
        }

        .sources-title {
          font-weight: 600;
          color: #4b5563;
          margin-bottom: 4px;
        }

        .source-item {
          color: #6b7280;
          margin: 2px 0;
          display: flex;
          align-items: center;
          gap: 4px;
        }

        .source-badge {
          background: #2563eb;
          color: white;
          padding: 2px 6px;
          border-radius: 4px;
          font-size: 10px;
          font-weight: 600;
        }

        .loading-indicator {
          display: flex;
          gap: 4px;
          padding: 12px 16px;
          background: white;
          border-radius: 16px;
          border-bottom-left-radius: 4px;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .loading-dot {
          width: 8px;
          height: 8px;
          background: #2563eb;
          border-radius: 50%;
          animation: bounce 1.4s ease-in-out infinite;
        }

        .loading-dot:nth-child(1) {
          animation-delay: -0.32s;
        }

        .loading-dot:nth-child(2) {
          animation-delay: -0.16s;
        }

        @keyframes bounce {
          0%, 80%, 100% {
            transform: scale(0);
            opacity: 0.5;
          }
          40% {
            transform: scale(1);
            opacity: 1;
          }
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
          transition: all 0.2s;
        }

        .chat-input input:focus {
          border-color: #2563eb;
          box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }

        .chat-input input:disabled {
          background: #f9fafb;
          cursor: not-allowed;
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

        .send-btn:hover:not(:disabled) {
          transform: scale(1.05);
          box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
        }

        .send-btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .send-btn svg {
          width: 20px;
          height: 20px;
          color: white;
        }

        @media (max-width: 768px) {
          .chat-window {
            right: 12px;
            bottom: 108px;
            width: calc(100vw - 24px);
          }

          .ai-float-container {
            right: 12px;
            bottom: 20px;
          }
        }
      `}</style>

      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <div className="chat-header-left">
              <div className="chat-avatar">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                </svg>
              </div>
              <div className="chat-title">
                <h3>Physical AI Assistant</h3>
                <p>RAG-powered • Always learning</p>
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
                <div className="message-bubble">
                  {msg.text}
                  
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="sources">
                      <div className="sources-title">📚 Sources:</div>
                      {msg.sources.map((source, idx) => (
                        <div key={idx} className="source-item">
                          <span className="source-badge">{(source.relevance_score * 100).toFixed(0)}%</span>
                          <span>{source.title}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
                <div className="message-time">{formatTime(msg.timestamp)}</div>
              </div>
            ))}
            
            {isLoading && (
              <div className="message bot">
                <div className="loading-indicator">
                  <div className="loading-dot"></div>
                  <div className="loading-dot"></div>
                  <div className="loading-dot"></div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about robotics, AI, ROS 2..."
              disabled={isLoading}
            />
            <button 
              className="send-btn" 
              onClick={handleSend}
              disabled={isLoading || !message.trim()}
            >
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
              </svg>
            </button>
          </div>
        </div>
      )}

      <div className="ai-float-container">
        <div className="ai-float-button" onClick={() => setIsOpen(!isOpen)}>
          <div className="pulse-ring"></div>
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
          </svg>
          <div className="online-indicator"></div>
        </div>
      </div>
    </>
  );
    </div>
  );
}
