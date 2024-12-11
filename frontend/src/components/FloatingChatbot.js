import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, MessageCircle, X } from 'lucide-react';

const FloatingChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { 
      id: 1, 
      text: 'Welcome to Rajasthan Technical Education Support. How can I help you today?', 
      sender: 'bot' 
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = { 
      id: messages.length + 1, 
      text: inputMessage, 
      sender: 'user' 
    };

    setMessages(prevMessages => [...prevMessages, userMessage]);
    setInputMessage('');

    try {
      const response = await axios.post('/api/chat', { message: inputMessage });
      const botResponse = { 
        id: messages.length + 2, 
        text: response.data.message, 
        sender: 'bot' 
      };
      setMessages(prevMessages => [...prevMessages, botResponse]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = { 
        id: messages.length + 2, 
        text: 'Sorry, I could not process your request. Please try again.', 
        sender: 'bot' 
      };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen ? (
        <div className="w-96 h-[500px] bg-white shadow-2xl rounded-xl flex flex-col border">
          <div className="bg-black text-white p-4 rounded-t-xl flex justify-between items-center">
            <h2 className="text-lg font-bold">PRAVESH</h2>
            <button 
              onClick={() => setIsOpen(false)} 
              className="hover:bg-gray-500 p-1 rounded-full"
            >
              <X size={24} />
            </button>
          </div>

          <div className="flex-grow bg-gradient-to-br from-green-100 via-green-300 to-yellow-200 overflow-y-auto p-4 space-y-3">
            {messages.map((msg) => (
              <div 
                key={msg.id} 
                className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div 
                  className={`max-w-[80%] p-3 ${
                    msg.sender === 'user' 
                      ? 'bg-blue-500 text-white rounded-3xl rounded-br-lg' 
                      : 'bg-gray-200 text-black rounded-3xl rounded-bl-lg'
                  }`}
                >
                  {msg.text}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <div className="p-4 border-t flex space-x-2">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Type your query..."
              className="flex-grow p-2 border rounded-lg"
            />
            <button 
              onClick={handleSendMessage} 
              className="bg-orange-500 text-white p-2 rounded-full hover:bg-orange-400"
            >
              <Send size={20} />
            </button>
          </div>
        </div>
      ) : (
        <button 
          onClick={() => setIsOpen(true)}
          className="bg-blue-600 text-white p-4 rounded-full shadow-2xl hover:bg-blue-700 transition-all"
        >
          <MessageCircle size={24} />
        </button>
      )}
    </div>
  );
};

export default FloatingChatbot;
