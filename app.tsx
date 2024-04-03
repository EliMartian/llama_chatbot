import React from 'react';
import Chatbot from './chatbot';

const App: React.FC = () => {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Financial Chatbot</h1>
      </header>
      <main>
        <Chatbot />
      </main>
    </div>
  );
};

export default App;
