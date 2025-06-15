import React, { useState } from 'react';
import axios from 'axios';

const ChatWindow: React.FC = () => {
  const [messages, setMessages] = useState<string[]>([]);
  const [input, setInput] = useState('');

  const handleSendMessage = async () => {
    if (!input.trim()) return;
    setMessages([...messages, "You: " + input]);
    const res = await axios.post('http://localhost:8000/chat', { message: input });
    setMessages(prev => [...prev, "GPT: " + res.data.reply]);
    setInput('');
  };

  return (
    <div className="p-4 bg-gray-900 text-white rounded h-full">
      <div className="overflow-y-scroll h-64 mb-2 bg-black p-2 rounded">
        {messages.map((msg, idx) => (
          <div key={idx} className="mb-1">{msg}</div>
        ))}
      </div>
      <input
        className="w-full p-2 rounded text-black"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
        placeholder="Ask ChatGPT..."
      />
    </div>
  );
};

export default ChatWindow;
