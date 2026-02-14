import React, { useState, useRef, useEffect } from 'react';

/**
 * ChatFlow — AI-powered chat component.
 * Sends messages to the backend AI agent and renders responses.
 */
export default function ChatFlow() {
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [sessionId, setSessionId] = useState(null);
    const [inputDisabled, setInputDisabled] = useState(false);
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);
    const initializedRef = useRef(false);

    // Scroll to bottom on new messages
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, isTyping]);

    // Focus input
    useEffect(() => {
        if (!inputDisabled) inputRef.current?.focus();
    }, [inputDisabled, messages]);

    // Send initial greeting on mount
    useEffect(() => {
        if (initializedRef.current) return;
        initializedRef.current = true;
        sendToAgent("Hi, I'd like to open a checking account.", true);
    }, []);

    async function sendToAgent(message, isAutoGreeting = false) {
        // Show user message (unless it's the auto-greeting)
        if (!isAutoGreeting) {
            setMessages(prev => [...prev, { type: 'user', text: message }]);
        }

        setIsTyping(true);
        setInputDisabled(true);

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, sessionId }),
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.detail || 'Server error');
            }

            // Update session
            if (data.sessionId) setSessionId(data.sessionId);

            // Build the bot message
            const botMsg = {
                type: 'bot',
                text: data.reply,
            };

            // Check if account was created (metadata from agent)
            if (data.metadata?.accountCreated) {
                botMsg.success = true;
                botMsg.accountData = {
                    accountNumber: data.metadata.accountNumber,
                    routingNumber: data.metadata.routingNumber,
                    accountType: data.metadata.accountType || 'Checking',
                };
            }

            setMessages(prev => [...prev, botMsg]);
            setInputDisabled(false);

        } catch (err) {
            setMessages(prev => [...prev, {
                type: 'bot',
                text: `❌ Sorry, I encountered an error: ${err.message}. Please try again.`,
                error: true,
            }]);
            setInputDisabled(false);
        } finally {
            setIsTyping(false);
        }
    }

    function handleSend() {
        const value = inputValue.trim();
        if (!value || inputDisabled) return;
        setInputValue('');
        sendToAgent(value);
    }

    function handleKeyDown(e) {
        if (e.key === 'Enter') handleSend();
    }

    return (
        <>
            <div className="chatbot-messages">
                {messages.map((msg, i) => (
                    <div key={i} className={`chat-message ${msg.type}`}>
                        <span className="msg-icon">{msg.type === 'bot' ? '🤖' : '👤'}</span>
                        <div className={`chat-bubble ${msg.error ? 'error' : ''} ${msg.success ? 'success' : ''}`}>
                            <div dangerouslySetInnerHTML={{ __html: formatMessageText(msg.text) }} />

                            {/* Success — account details */}
                            {msg.success && msg.accountData && (
                                <div className="account-details">
                                    <div className="detail-row">
                                        <span className="detail-label">Account Number</span>
                                        <span className="detail-value">{msg.accountData.accountNumber}</span>
                                    </div>
                                    <div className="detail-row">
                                        <span className="detail-label">Routing Number</span>
                                        <span className="detail-value">{msg.accountData.routingNumber}</span>
                                    </div>
                                    <div className="detail-row">
                                        <span className="detail-label">Account Type</span>
                                        <span className="detail-value">{msg.accountData.accountType}</span>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                {isTyping && <TypingIndicator />}
                <div ref={messagesEndRef} />
            </div>

            {/* Input area */}
            <div className="chatbot-input-area">
                <input
                    ref={inputRef}
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Type your message..."
                    disabled={inputDisabled}
                    autoComplete="off"
                />
                <button
                    className="chatbot-send-btn"
                    onClick={handleSend}
                    disabled={!inputValue.trim() || inputDisabled}
                    aria-label="Send message"
                >
                    ➤
                </button>
            </div>
        </>
    );
}

function TypingIndicator() {
    return (
        <div className="chat-message bot">
            <span className="msg-icon">🤖</span>
            <div className="chat-bubble">
                <div className="typing-indicator">
                    <span className="dot"></span>
                    <span className="dot"></span>
                    <span className="dot"></span>
                </div>
            </div>
        </div>
    );
}

/**
 * Format bot messages — supports **bold** and newlines
 */
function formatMessageText(text) {
    if (!text) return '';
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br/>');
}
