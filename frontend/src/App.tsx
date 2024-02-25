import React, { useState, useRef } from 'react';
import Webcam from 'react-webcam';
import WebcamControls from './components/WebcamControls';
import Navbar from './components/Navbar';
import { dataURLToBlob } from 'blob-util';
import WordListComponent from './components/WordListComponent';
import './App.css';

const App: React.FC = () => {
	const webcamRef = useRef<Webcam | null>(null);
	const [isWebcamActive, setIsWebcamActive] = useState(false);
	const [capturedImage, setCapturedImage] = useState<string | null>(null);
	const [wordList, setWordList] = useState([]);

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
			const response = await fetch('http://localhost:5000/upload', {
				method: 'POST',
				body: formData,
			});

			if (response.ok) {
				console.log('Image uploaded successfully!');

				const json = await response.json();
				if (json.ok) {
					setWordList(json.data);
				}
			} else {
				console.error('Upload failed:', response.statusText);
			}
		} catch (error) {
			console.error('Error uploading image:', error);
		}
	};

	return (
		<div className='App'>
			<Navbar title='grid gurus' />
			{isWebcamActive ? (
				<>
					<div className='webcam-container'>
						<Webcam
							audio={false}
							ref={webcamRef}
						/>
						<div className='centered-square'></div>
					</div>
				</>
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
			{wordList && <WordListComponent wordList={wordList} />}
		</div>
	);
};

export default App;
