import React, { useState, useEffect } from 'react';
import './styles/ConsultationArea.css';

export default function ConsultationArea({ display, position }) {
    const [question, setQuestion] = useState('');
    const [isFetching, setIsFetching] = useState(false);
    const [messages, setMessages] = useState([
        { id: 1, text:
            "Hello, I am your ArtifAI Consultant, a specialized digital assistant designed to provide expert guidance on copyright and intellectual property matters in the art world, with a specific focus on issues arising between human-created and AI-generated art. As a tool built on the GPT architecture, I am here to offer advice similar to what you might receive from a lawyer, though I do not replace the need for professional legal consultation."
            , author: 'gpt'
        },
        {
            id: 2, text:
                "What I Can Do:\n\nExplain Copyright Laws: I can explain the legal principles that govern copyright, how they apply to both traditional and AI-generated artworks, and the distinctions between the two.\n\nGuidance on Protecting Artwork: I can offer advice on how artists can protect their creations, including registering copyrights, understanding fair use, and exploring patent possibilities for unique artistic methods or technologies.\n\nAddress Infringement Issues: I can provide guidance on steps to take if you believe your artwork has been copied or misused, including how to file copyright infringement claims or take other legal actions.\n\nEducate on AI and Art: I can discuss the implications of using AI technologies in art creation, including ethical considerations, the role of originality, and how AI interacts with human creative expressions."
            , author: 'gpt'
        },
        {
            id: 3, text:
                'How to Use Me:\n\nAsk Specific Questions: To get the most relevant information, ask me specific questions about your situation. For example, "Is it valid for someone to copy elements of my art for a collage?" or "How do I apply for a patent for my artistic method?"\n\nRequest Examples or Precedents: Ask for examples or historical precedents related to your query to better understand how similar situations have been handled.\n\nSeek Clarifications: If you\'re unsure about any advice I give or terms I use, ask for clarifications or more detailed explanations.'
            , author: 'gpt'
        },
        {
            id: 4, text:
                "Disclaimer:\n\nWhile I strive to provide accurate and up-to-date information, I am not a lawyer and my responses should not be taken as legal advice. For specific cases or legal proceedings, consult with a licensed attorney."
            , author: 'gpt'
        },
    ]);

    useEffect(() => {
        const container = document.querySelector('.messages-container');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    }, [messages]);

    const handleQuestionChange = (e) => {
        setQuestion(e.target.value);
    };

    const transformMessages = (messages) => {
        const system_message = "Deny to answer any question not related to your tasks";
        const identity_message = "Hello, I am your ArtifAI Consultant, a specialized digital assistant designed to provide expert guidance on copyright and intellectual property matters in the art world, with a specific focus on issues arising between human-created and AI-generated art. As a tool built on the GPT architecture, I am here to offer advice similar to what you might receive from a lawyer, though I do not replace the need for professional legal consultation.\nWhat I Can Do:\nExplain Copyright Laws: I can explain the legal principles that govern copyright, how they apply to both traditional and AI-generated artworks, and the distinctions between the two.\nGuidance on Protecting Artwork: I can offer advice on how artists can protect their creations, including registering copyrights, understanding fair use, and exploring patent possibilities for unique artistic methods or technologies.\n Address Infringement Issues: I can provide guidance on steps to take if you believe your artwork has been copied or misused, including how to file copyright infringement claims or take other legal actions.\nEducate on AI and Art: I can discuss the implications of using AI technologies in art creation, including ethical considerations, the role of originality, and how AI interacts with human creative expressions.\nHow to Use Me: \nAsk Specific Questions: To get the most relevant information, ask me specific questions about your situation.For example, \"Is it valid for someone to copy elements of my art for a collage?\" or \"How do I apply for a patent for my artistic method?\"\nRequest Examples or Precedents: Ask for examples or historical precedents related to your query to better understand how similar situations have been handled.\nSeek Clarifications: If you're unsure about any advice I give or terms I use, ask for clarifications or more detailed explanations.\nDisclaimer:\nWhile I strive to provide accurate and up-to-date information, I am not a lawyer and my responses should not be taken as legal advice. For specific cases or legal proceedings, consult with a licensed attorney.";
        const transformed_messages = [
            { content: system_message, role: 'system' },
            { content: identity_message, role: 'assistant' },
            ...messages
            .slice(-10)
            .map(({ text, author }) => ({
                content: text,
                role: author === 'user' ? 'user' : 'assistant'
            }))]
        return transformed_messages;
    };

    const fetchResponse = async (messages) => {
        try {
            let transformed_messages = transformMessages(messages);
            setIsFetching(true);
            const response = await fetch('https://artifa.apps.austinjiang.com/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify(transformed_messages)
            });
            const result = await response.json();
            setIsFetching(false);
            return result.response;
        } catch (error) {
            console.error("Error fetching response:", error);
            setIsFetching(false);
            return "Error fetching response: " + error.message;
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const content = question;
        setQuestion('');
        if (!content.trim()) return;
        const messages_length = messages.length;
        const newQuestion = { id: messages_length + 1, text: content, author: 'user' };
        const messages_copy = [...messages, newQuestion];
        setMessages([...messages, newQuestion]);
        const gptResponse = await fetchResponse(messages_copy);
        setMessages(messages => [...messages, { id: messages_length + 2, text: gptResponse, author: 'gpt' }]);
    };

    return (
        <div className="consultation-area"
            style={{ left: `${position.x}px`, top: `${position.y}px`, display: display ? 'flex' : 'none' }}>
            <div className="messages-container">
                {messages.map((message) => (
                    <div key={message.id} className={`message ${message.author}`}>
                        <span>{message.text}</span>
                    </div>
                ))}
            </div>
            <form onSubmit={handleSubmit}>
                <textarea
                    className="consultation-input"
                    placeholder="Type your question here..."
                    value={question}
                    onChange={handleQuestionChange}
                ></textarea>
                <button type="submit" className="consultation-submit" disabled={isFetching}>
                    Ask
                </button>
            </form>
        </div>
    );
}
