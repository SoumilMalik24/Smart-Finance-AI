import React from 'react';
import { Plus, MessageSquare, Trash2, Github } from 'lucide-react';
import clsx from 'clsx'; // Helper for conditional classes

export function Sidebar({ sessions, activeSessionId, onSwitchSession, onNewChat, onDeleteSession }) {
    return (
        <div className="w-64 bg-finance-panel border-r border-finance-border flex flex-col h-full transition-all duration-300">

            {/* Header / Logo */}
            <div className="p-4 border-b border-finance-border flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg overflow-hidden flex items-center justify-center">
                    <img src="/logo.jpg" alt="Finance AI Logo" className="w-full h-full object-cover" />
                </div>
                <h1 className="text-finance-text font-bold text-lg tracking-tight">
                    Finance<span className="text-finance-accent">AI</span>
                </h1>
            </div>

            {/* New Chat Button */}
            <div className="p-4">
                <button
                    onClick={onNewChat}
                    className="w-full flex items-center gap-2 bg-finance-accent hover:bg-finance-accentHover text-white px-4 py-3 rounded-lg font-medium transition-colors shadow-lg shadow-finance-accent/20"
                >
                    <Plus size={20} />
                    <span>New Analysis</span>
                </button>
            </div>

            {/* Session List (Scrollable) */}
            <div className="flex-1 overflow-y-auto px-2 py-2 space-y-1">
                <h3 className="px-4 text-xs font-semibold text-finance-muted uppercase tracking-wider mb-2">
                    History
                </h3>

                {sessions.map((session) => (
                    <div key={session.id} className="group relative">
                        <button
                            onClick={() => onSwitchSession(session.id)}
                            className={clsx(
                                "w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm transition-colors text-left",
                                activeSessionId === session.id
                                    ? "bg-finance-surface text-finance-text"
                                    : "text-finance-muted hover:bg-finance-surface/50 hover:text-finance-text"
                            )}
                        >
                            <MessageSquare size={16} />
                            <span className="truncate">{session.title || "Untitled Session"}</span>
                        </button>

                        {/* Delete Button (Only visible on hover) */}
                        <button
                            onClick={(e) => {
                                e.stopPropagation();
                                onDeleteSession(session.id);
                            }}
                            className="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 text-finance-muted hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"
                        >
                            <Trash2 size={14} />
                        </button>
                    </div>
                ))}

                {sessions.length === 0 && (
                    <div className="text-center py-10 px-4">
                        <p className="text-finance-muted text-sm">No history yet.</p>
                    </div>
                )}
            </div>

            {/* Footer */}
            <div className="p-4 border-t border-finance-border text-finance-muted text-xs flex items-center justify-between">
                <span>v1.0.0 MVP</span>
                <a href="#" className="hover:text-finance-text"><Github size={14} /></a>
            </div>
        </div>
    );
}