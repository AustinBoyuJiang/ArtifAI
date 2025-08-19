import React, { useState } from 'react';
import FileUploader from './FileUploader';
import ResultArea from './ResultArea';
import BackgroundImage from './assets/background.png';
import './styles/HomePage.css';

let resultID = 0;
let buttonDisplay = false;

export default function HomePage() {
    const [file, setFile] = useState(null);
    const [uploadedImages, setUploadedImages] = useState([]);

    const handleFileSelect = (selectedFile) => {
        setFile(selectedFile);
        buttonDisplay = true;
    };

    const handleDetect = () => {
        console.log("Detecting the image...");
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setUploadedImages(prevImages => [{'img': reader.result,'id': resultID, 'name': file.name }, ...prevImages]);
                resultID++;
            };
            reader.readAsDataURL(file);
            setFile(null);
        }
    };

    return (
        <div className="home-container">
            <div className="content-wrapper">
                {/*<img className="background-image" src={BackgroundImage} />*/}
                <div className="left-side">
                    <h1>Discover ArtifAI: Bridging Human Creativity and AI Innovation</h1>
                    <p>Detecting the potential origin of an artwork, ArtifAI is your ally in addressing the evolving landscape of copyright and rights in the digital age.</p>
                </div>
                <div className="right-side">
                    <FileUploader onFileSelect={handleFileSelect} />
                    {buttonDisplay && <button onClick={handleDetect} className="detect-button">Detect</button>}
                </div>
            </div>
            {uploadedImages.length > 0 && (
                <div>
                    <div className="scroll-down-indicator">
                        <span>Scroll down to see results</span>
                        <div className="line"></div>
                    </div>
                    {uploadedImages.map((img, index) => (
                        <div key={index}>
                            {/* Conditionally display headers */}
                            {index === 0 && (
                                <h2 className="result-header">Newest Result</h2>
                            )}
                            {index === 1 && uploadedImages.length > 1 && (
                                <h2 className="result-header">Result History</h2>
                            )}
                            <ResultArea img={img.img} id={img.id} fileName={img.name }/>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
