import React, { useRef, useState } from 'react';
import './styles/FileUploader.css'; // Ensure your CSS is correctly linked
import uploadImage from './assets/upload.png';
import uploadedImage from './assets/image.png';

export default function FileUploader({ onFileSelect }) {
    const [fileName, setFileName] = useState('');
    const [fileSelected, setFileSelected] = useState(false);
    const fileInputRef = useRef(null); // Use useRef to access the file input element

    const handleBoxClick = () => {
        // Directly open the file chooser dialog
        fileInputRef.current.click();
    };

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file && (file.type === "image/jpeg" || file.type === "image/png")) {
            setFileName(file.name);
            setFileSelected(true);
            onFileSelect(file); // Notify the parent component
        }
    };

    return (
        <div className="upload-box" onClick={handleBoxClick}>
            <input
                type="file"
                id="file-upload"
                onChange={handleFileChange}
                accept="image/jpeg,image/png"
                style={{ display: 'none' }}
                ref={fileInputRef} // Attach the ref to the input
            />
            <div>
                {!fileSelected ? (
                    <div className="upload-content">
                        <img src={uploadImage} alt="Upload" className="upload-icon" />
                        <p>Upload your image here</p>
                    </div>
                ) : (
                    <div className="upload-content">
                        <img src={uploadedImage} alt="Uploaded" className="upload-icon" />
                        <p>{fileName}</p>
                    </div>
                )}
            </div>
        </div>
    );
}
