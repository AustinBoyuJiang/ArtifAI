import React, { useState, useRef } from 'react';
import './styles/DraggableCircle.css';
import ConsultationArea from './ConsultationArea';
import MessageImage from './assets/message.png';

const consultationArea_x = [80, -660];
const consultationArea_y = [10, -440];

export default function DraggableCircle() {
    const [position, setPosition] = useState({ x: window.innerWidth - 200, y: window.innerHeight-150 }); // Initial position
    const [dragging, setDragging] = useState(true);
    const [expanded, setExpanded] = useState(false);
    const [expanding, setExpanding] = useState(false);
    const [showDot, setShowDot] = useState(true);
    const dragItem = useRef(null); // Ref to track the click position within the circle

    const handleDragging = (e) => {
        setExpanding(false);
        if (dragging) {
            const mouseX = e.clientX - dragItem.current.offsetX;
            const mouseY = e.clientY - dragItem.current.offsetY;
            setPosition({ x: mouseX, y: mouseY });
        }
    };

    const handleDragStart = (e) => {
        document.addEventListener('mousemove', handleDragging);
        setDragging(true);
        setExpanding(true);
        dragItem.current = {
            offsetX: e.clientX - position.x,
            offsetY: e.clientY - position.y,
        };
    };

    const handleDragEnd = () => {
        if (expanding) {
            setExpanded(!expanded);
            setShowDot(false);
        }
        document.removeEventListener('mousemove', handleDragging);
        setDragging(false);
        dragItem.current = null;
    };

    const handleMouseLeave = () => {
        setExpanding(false);
    };

    return (
        <div
            className="draggable-circle"
            style={{ left: `${position.x}px`, top: `${position.y}px` }}>
            <div
                className="event-handler"
                onMouseDown={handleDragStart}
                onMouseUp={handleDragEnd}
                onMouseLeave={handleMouseLeave }
            >
                {showDot && (
                    <div className="red-dot">
                        <span className="dot-text">4</span>
                    </div>
                )}
                <img className='message-image' src={MessageImage} draggable="false" />
            </div>
            <ConsultationArea
                display={expanded}
                position={{ x: consultationArea_x[position.x > 400 ? 1 : 0], y: consultationArea_y[position.y > 300 ? 1 : 0] }}
            />
        </div>
    );
}
