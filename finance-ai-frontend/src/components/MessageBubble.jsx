import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Bot, User } from 'lucide-react';
import clsx from 'clsx';

export function MessageBubble({ role, content, charts }) {
    const isUser = role === 'user';

    // Don't render empty assistant messages (placeholder before first token)
    if (!isUser && !content && (!charts || charts.length === 0)) return null;

    return (
        <div className={clsx(
            "flex gap-4 px-6 py-5 border-b border-finance-border/30",
            isUser ? "bg-finance-bg" : "bg-finance-panel/30"
        )}>
            {/* Avatar */}
            <div className={clsx(
                "w-8 h-8 rounded-lg flex items-center justify-center shrink-0 mt-0.5",
                isUser ? "bg-finance-surface" : "bg-finance-accent"
            )}>
                {isUser ? <User size={16} /> : <Bot size={16} className="text-white" />}
            </div>

            {/* Content */}
            <div className="flex-1 min-w-0 max-w-4xl">
                <div className="font-semibold text-xs mb-1.5 text-finance-muted uppercase tracking-wider">
                    {isUser ? "You" : "Finance AI"}
                </div>

                {isUser ? (
                    <p className="text-finance-text leading-relaxed whitespace-pre-wrap">{content}</p>
                ) : (
                    <>
                        {/* Text content rendered as markdown */}
                        {content && (
                            <div className="prose prose-invert prose-sm prose-p:leading-relaxed prose-pre:bg-finance-bg prose-pre:border prose-pre:border-finance-border prose-table:text-sm max-w-none text-finance-text">
                                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                    {content}
                                </ReactMarkdown>
                            </div>
                        )}

                        {/* Chart images rendered directly as <img> tags */}
                        {charts && charts.length > 0 && (
                            <div className="mt-4 space-y-4">
                                {charts.map((src, idx) => (
                                    <div key={idx} className="rounded-xl overflow-hidden border border-finance-border shadow-lg bg-white">
                                        <img
                                            src={src}
                                            alt={`Financial Chart ${idx + 1}`}
                                            className="w-full h-auto block"
                                        />
                                    </div>
                                ))}
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
}