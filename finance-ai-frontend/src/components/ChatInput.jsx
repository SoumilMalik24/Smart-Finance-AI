import React, { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';

export function ChatInput({ onSend, isLoading }) {
  const [input, setInput] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    
    onSend(input);
    setInput(""); // Clear input after sending
  };

  return (
    <div className="p-4 bg-finance-bg border-t border-finance-border">
      <form 
        onSubmit={handleSubmit}
        className="max-w-4xl mx-auto relative flex items-center"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={isLoading ? "AI is thinking..." : "Ask about finance, math, or investments..."}
          disabled={isLoading}
          className="w-full bg-finance-panel text-finance-text placeholder-finance-muted rounded-xl pl-4 pr-12 py-4 focus:outline-none focus:ring-2 focus:ring-finance-accent/50 border border-finance-border shadow-sm transition-all"
        />
        
        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className="absolute right-2 p-2 bg-finance-accent hover:bg-finance-accentHover disabled:opacity-50 disabled:cursor-not-allowed rounded-lg text-white transition-colors"
        >
          {isLoading ? (
            <Loader2 size={20} className="animate-spin" />
          ) : (
            <Send size={20} />
          )}
        </button>
      </form>
      
      <p className="text-center text-xs text-finance-muted mt-2">
        AI can make mistakes. Please double-check financial data.
      </p>
    </div>
  );
}