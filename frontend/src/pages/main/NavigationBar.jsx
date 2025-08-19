import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import './styles/NavigationBar.css';
import Icon from "./assets/icon.png"

export default function NavigationBar() {
    const [isVisible, setIsVisible] = useState(true);

    useEffect(() => {
        let lastScrollY = window.scrollY;

        const handleScroll = () => {
            setIsVisible(lastScrollY >= window.scrollY);
            lastScrollY = window.scrollY;
        };

        window.addEventListener('scroll', handleScroll, { passive: true });

        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <div className={`navigation-bar ${isVisible ? '' : 'navigation-bar-hidden'}`}>
            <img src={Icon} className="navbar-logo-icon" alt="Logo" href='/'/>
            <span className="navbar-logo-text">ArtifAI</span>
            <NavLink to="/" className={({ isActive }) => (isActive ? 'nav-link-active' : '')}>HOME</NavLink>
            <NavLink to="/about" className={({ isActive }) => (isActive ? 'nav-link-active' : '')}>ABOUT</NavLink>
            <NavLink to="/faq" className={({ isActive }) => (isActive ? 'nav-link-active' : '')}>FAQ</NavLink>
            <NavLink to="/api" className={({ isActive }) => (isActive ? 'nav-link-active' : '')}>API</NavLink>
            <NavLink to="/team" className={({ isActive }) => (isActive ? 'nav-link-active' : '')}>TEAM</NavLink>
            <NavLink to="/contact" className={({ isActive }) => (isActive ? 'nav-link-active' : '')}>CONTACT</NavLink>
        </div>
    );
}
