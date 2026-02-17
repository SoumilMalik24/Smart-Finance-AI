import React, { useEffect, useRef } from 'react';
import { MessageBubble } from './MessageBubble';
import { ChatInput } from './ChatInput';
import { Loader2, TrendingUp, Calculator, PiggyBank } from 'lucide-react';

const SUGGESTIONS = [
    { icon: TrendingUp, text: "Show me 5-year investment growth at 12% return" },
    { icon: Calculator, text: "Calculate my savings rate if I earn ₹80,000 and spend ₹50,000" },
    { icon: PiggyBank, text: "How much emergency fund do I need for ₹30,000 monthly expenses?" },
];

export function ChatWindow({ messages, onSend, isLoading, activeTool }) {
    const bottomRef = useRef(null);

    // Auto-scroll to bottom when messages change
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, activeTool]);

    return (
        <div className="flex flex-col h-full w-full bg-finance-bg">

            {/* Messages List */}
            <div className="flex-1 overflow-y-auto min-h-0">
                {messages.length === 0 ? (
                    /* Welcome Screen */
                    <div className="h-full flex flex-col items-center justify-center px-6">
                        <div className="w-16 h-16 bg-finance-accent/10 border border-finance-accent/20 rounded-2xl flex items-center justify-center mb-4">
                            <span className="text-3xl">💰</span>
                        </div>
                        <h2 className="text-xl font-semibold text-finance-text mb-2">Smart Finance AI</h2>
                        <p className="text-finance-muted text-sm mb-8 text-center max-w-md">
                            Your AI-powered financial advisor. Ask about investments, savings, expenses, and more.
                        </p>

                        {/* Suggestion Cards */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 max-w-3xl w-full">
                            {SUGGESTIONS.map((suggestion, idx) => (
                                <button
                                    key={idx}
                                    onClick={() => onSend(suggestion.text)}
                                    className="text-left p-4 rounded-xl border border-finance-border bg-finance-panel/50 hover:bg-finance-panel hover:border-finance-accent/30 transition-all group"
                                >
                                    <suggestion.icon size={18} className="text-finance-accent mb-2 group-hover:scale-110 transition-transform" />
                                    <p className="text-sm text-finance-muted group-hover:text-finance-text transition-colors">
                                        {suggestion.text}
                                    </p>
                                </button>
                            ))}
                        </div>
                    </div>
                ) : (
                    <>
                        {messages.map((msg, idx) => (
                            <MessageBubble key={idx} role={msg.role} content={msg.content} charts={msg.charts} />
                        ))}
                    </>
                )}

                {/* Tool Indicator */}
                {activeTool && (
                    <div className="flex items-center gap-2 px-6 py-4 text-sm text-finance-muted">
                        <Loader2 size={16} className="animate-spin text-finance-accent" />
                        <span>
                            Using tool: <span className="font-mono text-finance-accent">{activeTool}</span>...
                        </span>
                    </div>
                )}

                {/* Typing indicator when loading but no tool active */}
                {isLoading && !activeTool && messages.length > 0 && messages[messages.length - 1]?.content === '' && (
                    <div className="flex items-center gap-2 px-6 py-4 text-sm text-finance-muted">
                        <div className="flex gap-1">
                            <span className="w-1.5 h-1.5 bg-finance-accent rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                            <span className="w-1.5 h-1.5 bg-finance-accent rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                            <span className="w-1.5 h-1.5 bg-finance-accent rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                        </div>
                        <span>Thinking...</span>
                    </div>
                )}

                <div ref={bottomRef} />
            </div>

            {/* Input Area */}
            <ChatInput onSend={onSend} isLoading={isLoading} />
        </div>
    );
}