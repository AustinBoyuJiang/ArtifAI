import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import ParticlesBackground from "./ParticlesBackground";
import "./styles/MainPage.css";
import NavigationBar from "./NavigationBar";
import Footer from "./Footer";
import HomePage from "../home/HomePage";
import AboutPage from "../about/AboutPage";
import FAQPage from "../faq/FAQPage";
import APIPage from "../api/APIPage";
import TeamPage from "../team/TeamPage";
import ContactPage from "../contact/ContactPage";
import ErrorPage from "../error/ErrorPage";
import DraggableCircle from './DraggableCircle';

// This component is created to use the useLocation hook
function ContentWithRouting() {
    let location = useLocation();
    const isHome = location.pathname === '/';

    return (
        <div style={{ display: isHome ? 'block' : 'none' }}>
            <HomePage />
        </div>
    );
}

export default function MainPage() {
    return (
        <Router>
            <div>
                <ParticlesBackground className="background"/>
                <NavigationBar />
                <ContentWithRouting />
                <Routes>
                    {/* Define a Route for HomePage but don't render anything to prevent duplication */}
                    <Route path="/" element={<></>} />
                    <Route path="/about" element={<AboutPage />} />
                    <Route path="/faq" element={<FAQPage />} />
                    <Route path="/api" element={<APIPage />} />
                    <Route path="/team" element={<TeamPage />} />
                    <Route path="/contact" element={<ContactPage />} />
                    <Route path="*" element={<ErrorPage />} />
                </Routes>
                <DraggableCircle />
                <Footer />
            </div>
        </Router>
    );
}
