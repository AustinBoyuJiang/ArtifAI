import React, { useState } from 'react';
import emailjs from 'emailjs-com';
import "./styles/ContactPage.css";

export default function ContactPage() {
    const [feedbackMessage, setFeedbackMessage] = useState('');
    const [email, setEmail] = useState('');

    const sendEmail = (e) => {
        e.preventDefault();

        // Check if email is empty
        if (!email.trim()) {
            setFeedbackMessage('Email cannot be empty.');
            return; // Stop the function if email is empty
        }

        emailjs.sendForm('service_akt7svy', 'template_qjaurls', e.target, 'tVcY2tcDyENLexWN0')
            .then((result) => {
                setFeedbackMessage('Message sent successfully!');
                console.log(result.text);
            }, (error) => {
                setFeedbackMessage('Failed to send the message, please try again.');
                console.log(error.text);
            });

        // Assuming you want to reset the form and clear the email state
        e.target.reset();
        setEmail(''); // Clear email state after sending
    };

    // Update email state on change
    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };

    return (
        <div className="contact-container">
            <h1>Contact Us</h1>
            <form className="contact-form" onSubmit={sendEmail}>
                <label htmlFor="name">Name</label>
                <input type="text" id="name" name="name" placeholder="Your name..." />
                <label htmlFor="email">Email</label>
                <input type="email" id="email" name="email" placeholder="Your email..." onChange={handleEmailChange} value={email} />
                <label htmlFor="message">Message</label>
                <textarea id="message" name="message" placeholder="Write something..." ></textarea>
                <button type="submit">Send</button>
            </form>
            {feedbackMessage && <p>{feedbackMessage}</p>}
        </div>
    );
}
