import React, { useState, useRef } from 'react';
import Webcam from 'react-webcam';
import WebcamControls from './WebcamControls';
import { dataURLToBlob } from 'blob-util';

const App: React.FC = () => {
	const webcamRef = useRef<Webcam | null>(null);
	const [isWebcamActive, setIsWebcamActive] = useState(false);
	const [capturedImage, setCapturedImage] = useState<string | null>(null);

	const handleStartWebcam = () => {
		setIsWebcamActive(true);
		setCapturedImage(null);
	};

	const handleCaptureImage = () => {
		if (webcamRef.current) {
			// Make sure webcamRef.current exists
			const imageSrc = webcamRef.current.getScreenshot();
			setCapturedImage(imageSrc);
			setIsWebcamActive(false);
		} else {
			console.error('Webcam is not ready yet');
		}
	};

	const handleUploadImage = async () => {
		if (!capturedImage) return;

		const blob = await dataURLToBlob(capturedImage);
		const formData = new FormData();
		formData.append('image', blob, 'image.png');

		// TODO: change backend url
		try {
			const response = await fetch('http://localhost:3000/upload', {
				method: 'POST',
				body: formData,
			});

			if (response.ok) {
				console.log('Image uploaded successfully!');
			} else {
				console.error('Upload failed:', response.statusText);
			}
		} catch (error) {
			console.error('Error uploading image:', error);
		}
	};

	return (
		<div className='App'>
			{isWebcamActive ? (
				<Webcam
					audio={false}
					ref={webcamRef}
				/>
			) : capturedImage ? (
				<img
					src={capturedImage}
					alt='Captured'
				/>
			) : (
				<p>Webcam is not active</p>
			)}
			<WebcamControls
				onStart={handleStartWebcam}
				onCapture={handleCaptureImage}
				onUpload={handleUploadImage}
				isCaptureDisabled={!isWebcamActive}
				isUploadDisabled={!capturedImage}
			/>
		</div>
	);
};

export default App;
