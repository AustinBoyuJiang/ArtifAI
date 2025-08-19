import React, { useState, useEffect } from 'react';
import './styles/FeedbackArea.css';

export default function FeedbackArea() {
    const [feedbackState, setFeedbackState] = useState('initial');
    const [showThankYou, setShowThankYou] = useState(false);

    useEffect(() => {
        let timer;
        if (showThankYou) {
            timer = setTimeout(() => {
                setFeedbackState('hidden');
                setShowThankYou(false); // Reset for next time the component is used
            }, 2000); // Display "Thank you" message for 2 seconds before hiding
        }
        return () => clearTimeout(timer);
    }, [showThankYou]);

    const handleMouseEnter = () => {
        if (feedbackState !== 'clicked' && feedbackState !== 'hidden' && !showThankYou) {
            setFeedbackState('hovered');
        }
    };

    const handleMouseLeave = () => {
        if (feedbackState === 'hovered') {
            setFeedbackState('initial');
        }
    };

    const handleFeedbackClick = () => {
        setShowThankYou(true);
    };

    let feedbackButtonsClass = 'feedback-buttons';
    if (feedbackState === 'hovered') {
        feedbackButtonsClass += ' visible';
    } else if (feedbackState === 'clicked' || feedbackState === 'hidden') {
        feedbackButtonsClass += ' fade-out';
    }

    return (
        <div className="feedback-container" onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
            {feedbackState !== 'hidden' && !showThankYou && feedbackState !== 'hovered' && (
                <div className="feedback-hover-trigger">
                    Feedback &lt;
                </div>
            )}
            {showThankYou ? (
                <div className="thank-you-message fade-in">Thanks for your feedback!</div>
            ) : (
                (feedbackState === 'hovered' || feedbackState === 'clicked') && (
                    <div className={feedbackButtonsClass}>
                        <button onClick={handleFeedbackClick} className='feedback-button good'>👻 Good Result</button>
                        <button onClick={handleFeedbackClick} className='feedback-button bad'>🥺 Bad Result</button>
                    </div>
                )
            )}
        </div>
    );
}