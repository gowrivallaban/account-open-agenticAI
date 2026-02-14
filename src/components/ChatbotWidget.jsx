import React, { useState, useRef, useEffect, forwardRef, useImperativeHandle } from 'react';
import ChatFlow from './ChatFlow';

const ChatbotWidget = forwardRef(function ChatbotWidget(props, ref) {
    const [isOpen, setIsOpen] = useState(false);

    useImperativeHandle(ref, () => ({
        open: () => setIsOpen(true),
    }));

    return (
        <>
            {/* Floating Action Button */}
            {!isOpen && (
                <button
                    id="chatbot-fab"
                    className="chatbot-fab"
                    onClick={() => setIsOpen(true)}
                    aria-label="Open AI Assistant"
                >
                    💬
                </button>
            )}

            {/* Chat Panel */}
            {isOpen && (
                <div className="chatbot-panel" role="dialog" aria-label="AI Banking Assistant">
                    <div className="chatbot-header">
                        <div className="chatbot-header-info">
                            <div className="chatbot-avatar">🤖</div>
                            <div className="chatbot-header-text">
                                <h4>GPS AI Assistant</h4>
                                <span>Online — Ready to help</span>
                            </div>
                        </div>
                        <button
                            className="chatbot-close"
                            onClick={() => setIsOpen(false)}
                            aria-label="Close chat"
                        >
                            ✕
                        </button>
                    </div>

                    <ChatFlow />
                </div>
            )}
        </>
    );
});

export default ChatbotWidget;
