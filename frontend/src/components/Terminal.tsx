import React, { useEffect } from 'react';
import { Terminal } from 'xterm';
import 'xterm/css/xterm.css';

const TerminalComponent: React.FC = () => {
  useEffect(() => {
    const term = new Terminal();
    term.open(document.getElementById('terminal') as HTMLElement);
    term.write('Welcome to DevGPT Terminal\r\n');

    term.onData(async (input) => {
      const res = await fetch('http://localhost:8000/exec', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: input, language: 'python' })
      });
      const { output } = await res.json();
      term.write('\r\n' + output + '\r\n');
    });
  }, []);

  return <div id="terminal" style={{ height: '300px', backgroundColor: '#000' }} />;
};

export default TerminalComponent;
