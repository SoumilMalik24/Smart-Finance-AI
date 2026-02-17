import React, { useState, useEffect, useRef } from 'react';
import { Sidebar } from './components/Sidebar';
import { ChatWindow } from './components/ChatWindow';
import { useChat } from './hooks/useChat';

function App() {
  // Session state
  const [sessions, setSessions] = useState([
    { id: 'default', title: 'Welcome to Finance AI' }
  ]);
  const [activeSessionId, setActiveSessionId] = useState('default');

  // Chat hook — tied to activeSessionId
  const { messages, sendMessage, isLoading, activeTool, clearMessages } = useChat(activeSessionId);

  // Store messages per session
  const sessionMessagesRef = useRef({ default: [] });

  // When activeSessionId changes, save old messages and restore new ones
  const prevSessionRef = useRef(activeSessionId);
  useEffect(() => {
    if (prevSessionRef.current !== activeSessionId) {
      // Save current messages for the OLD session
      sessionMessagesRef.current[prevSessionRef.current] = messages;
      prevSessionRef.current = activeSessionId;
      // Clear messages for the hook (new session starts fresh)
      clearMessages();
    }
  }, [activeSessionId, messages, clearMessages]);

  // Auto-title: update session title from first user message
  useEffect(() => {
    if (messages.length > 0) {
      const firstUserMsg = messages.find(m => m.role === 'user');
      if (firstUserMsg) {
        setSessions(prev =>
          prev.map(s =>
            s.id === activeSessionId && (s.title === 'New Analysis' || s.title === 'Welcome to Finance AI')
              ? { ...s, title: firstUserMsg.content.slice(0, 40) + (firstUserMsg.content.length > 40 ? '...' : '') }
              : s
          )
        );
      }
    }
  }, [messages, activeSessionId]);

  const handleNewChat = () => {
    const newId = Date.now().toString();
    setSessions(prev => [{ id: newId, title: 'New Analysis' }, ...prev]);
    setActiveSessionId(newId);
  };

  const handleDeleteSession = (id) => {
    const updated = sessions.filter(s => s.id !== id);
    delete sessionMessagesRef.current[id];

    if (updated.length === 0) {
      // Create fresh session if all deleted
      const newId = Date.now().toString();
      setSessions([{ id: newId, title: 'New Analysis' }]);
      setActiveSessionId(newId);
    } else {
      setSessions(updated);
      if (activeSessionId === id) {
        setActiveSessionId(updated[0].id);
      }
    }
  };

  return (
    <div className="flex h-screen bg-finance-bg text-finance-text font-sans overflow-hidden selection:bg-finance-accent/30">

      {/* Left Sidebar */}
      <Sidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        onSwitchSession={setActiveSessionId}
        onNewChat={handleNewChat}
        onDeleteSession={handleDeleteSession}
      />

      {/* Right Main Content Area */}
      <main className="flex-1 flex flex-col relative h-full w-full min-w-0">

        {/* Header */}
        <header className="h-14 border-b border-finance-border flex items-center justify-between px-6 bg-finance-bg/80 backdrop-blur-md z-10 shrink-0">
          <div className="flex items-center gap-3">
            <h2 className="font-semibold text-finance-text text-lg truncate max-w-md">
              {sessions.find(s => s.id === activeSessionId)?.title || "New Chat"}
            </h2>
          </div>

          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${isLoading ? 'bg-amber-400 animate-pulse' : 'bg-green-500'}`}></div>
            <span className="text-xs font-mono text-finance-muted">
              {isLoading ? 'PROCESSING' : 'READY'}
            </span>
          </div>
        </header>

        {/* Chat Interface */}
        <div className="flex-1 overflow-hidden relative flex flex-col min-h-0">
          <ChatWindow
            messages={messages}
            onSend={sendMessage}
            isLoading={isLoading}
            activeTool={activeTool}
          />
        </div>

      </main>
    </div>
  );
}

export default App;