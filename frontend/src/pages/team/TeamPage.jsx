import React from 'react';
import "./styles/TeamPage.css";
import AustinJiangPhoto from './assets/Austin Jiang.jpg'; 

export default function TeamPage() {
    return (
        <div className="team-container">
            <div className="team-member">
                <img src={AustinJiangPhoto} alt="Austin Jiang" className="member-photo" />
                <div className="member-info">
                    <h2>Hi, I am Austin</h2>
                    <p>I am an IB Diploma student living in West Vancouver, Canada. I am a coding enthusiast, particularly in competitive programming. I achieved platinum division in USACO and qualified for the Canadian Computing Olympiad by being a top participant in CCC. In my free time, I develop some personal projects addressing social issues. I am also a coding instructor at a local academy to teach kids to code.</p>
                    <p>Feel free to contact me through my personal website at <a href="http://aj-coder.com" target="_blank" rel="noopener noreferrer">aj-coder.com</a>.</p>
                </div>
            </div>
        </div>
    );
}
