import React from 'react';

type WebcamControlsProps = {
	onStart: () => void;
	onCapture: () => void;
	onUpload: () => void;
	isCaptureDisabled: boolean;
	isUploadDisabled: boolean;
};

const WebcamControls: React.FC<WebcamControlsProps> = ({
	onStart,
	onCapture,
	onUpload,
	isCaptureDisabled,
	isUploadDisabled,
}) => {
	return (
		<div>
			<button onClick={onStart}>Start Webcam</button>
			<button
				onClick={onCapture}
				disabled={isCaptureDisabled}
			>
				Capture Image
			</button>
			<button
				onClick={onUpload}
				disabled={isUploadDisabled}
			>
				Upload Image
			</button>
		</div>
	);
};

export default WebcamControls;
