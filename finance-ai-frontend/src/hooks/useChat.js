import { useState, useCallback } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export function useChat(sessionId) {
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [activeTool, setActiveTool] = useState(null);

    const sendMessage = useCallback(async (userText) => {
        if (!userText.trim() || isLoading) return;

        setIsLoading(true);
        setActiveTool(null);

        // Add user message + empty assistant placeholder
        setMessages((prev) => [
            ...prev,
            { role: "user", content: userText },
            { role: "assistant", content: "", charts: [] },
        ]);

        try {
            const response = await fetch(`${API_URL}/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ session_id: sessionId, message: userText }),
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });

                // Split by double newline (SSE delimiter)
                const parts = buffer.split("\n\n");
                buffer = parts.pop(); // Keep incomplete last chunk

                for (const part of parts) {
                    const trimmed = part.trim();
                    if (!trimmed.startsWith("data: ")) continue;

                    const jsonStr = trimmed.slice(6);
                    if (jsonStr === "[DONE]") {
                        setIsLoading(false);
                        setActiveTool(null);
                        continue;
                    }

                    try {
                        const data = JSON.parse(jsonStr);

                        switch (data.type) {
                            case "token":
                                // Append token to the last (assistant) message
                                setMessages((prev) => {
                                    const updated = [...prev];
                                    const lastIndex = updated.length - 1;
                                    updated[lastIndex] = {
                                        ...updated[lastIndex],
                                        content: updated[lastIndex].content + data.content,
                                    };
                                    return updated;
                                });
                                break;

                            case "chart":
                                // Add chart image to the last assistant message's charts array
                                setMessages((prev) => {
                                    const updated = [...prev];
                                    const lastIndex = updated.length - 1;
                                    const lastMsg = updated[lastIndex];
                                    updated[lastIndex] = {
                                        ...lastMsg,
                                        charts: [...(lastMsg.charts || []), data.src],
                                    };
                                    return updated;
                                });
                                break;

                            case "tool_start":
                                setActiveTool(data.tool);
                                break;

                            case "tool_end":
                                setActiveTool(null);
                                break;

                            case "status":
                                break;

                            case "done":
                                setIsLoading(false);
                                setActiveTool(null);
                                break;

                            case "error":
                                console.error("Backend error:", data.content);
                                setMessages((prev) => {
                                    const updated = [...prev];
                                    const lastIndex = updated.length - 1;
                                    updated[lastIndex] = {
                                        ...updated[lastIndex],
                                        content: `⚠️ Error: ${data.content}`,
                                    };
                                    return updated;
                                });
                                setIsLoading(false);
                                break;
                        }
                    } catch (e) {
                        console.warn("Failed to parse SSE chunk:", jsonStr, e);
                    }
                }
            }

            // Stream ended
            setIsLoading(false);
            setActiveTool(null);
        } catch (error) {
            console.error("Connection error:", error);
            setMessages((prev) => {
                const updated = [...prev];
                const lastIndex = updated.length - 1;
                if (lastIndex >= 0 && updated[lastIndex].role === "assistant") {
                    updated[lastIndex] = {
                        ...updated[lastIndex],
                        content: `⚠️ Connection failed: ${error.message}`,
                    };
                }
                return updated;
            });
            setIsLoading(false);
            setActiveTool(null);
        }
    }, [sessionId, isLoading]);

    const clearMessages = useCallback(() => {
        setMessages([]);
        setActiveTool(null);
        setIsLoading(false);
    }, []);

    return { messages, sendMessage, isLoading, activeTool, clearMessages };
}