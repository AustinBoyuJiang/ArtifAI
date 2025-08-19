import React from 'react';
import { Link } from 'react-router-dom';
import './styles/ErrorPage.css'; // Assume you have some basic styling

export default function ErrorPage() {
    return (
        <div className="error-container">
            <h1>404 - Page Not Found</h1>
            <p>The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.</p>
            <Link to="/">Go to HomePage</Link>
        </div>
    );
}
