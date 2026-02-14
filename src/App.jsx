import React, { useState, useRef } from 'react'
import LandingPage from './components/LandingPage'
import ChatbotWidget from './components/ChatbotWidget'

function App() {
    const chatbotRef = useRef(null);

    const openChatbot = () => {
        if (chatbotRef.current) {
            chatbotRef.current.open();
        }
    };

    return (
        <>
            <LandingPage onOpenChatbot={openChatbot} />
            <ChatbotWidget ref={chatbotRef} />
        </>
    )
}

export default App
