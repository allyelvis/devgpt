'use client';

import React from 'react';
import ChatWindow from '../components/ChatWindow';
import TerminalComponent from '../components/Terminal';

export default function Home() {
  return (
    <div className="flex flex-col md:flex-row gap-4 p-6 h-screen">
      <div className="flex-1">
        <ChatWindow />
      </div>
      <div className="flex-1">
        <TerminalComponent />
      </div>
    </div>
  );
}
