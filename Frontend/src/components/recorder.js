import React, { useState, useRef, useEffect } from 'react';

function WebcamRecorder() {
    const [isRecording, setIsRecording] = useState(false);
    const [stream, setStream] = useState(null);
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const mediaRecorderRef = useRef(null);
    const recordedChunks = useRef([]);
    const captureInterval = useRef(null);

    useEffect(() => {
        startRecording()
        function handleResize() {
            if (videoRef.current && canvasRef.current) {
                const videoHeight = window.innerHeight * 0.9;
                videoRef.current.style.maxHeight = `${videoHeight}px`;
                canvasRef.current.style.maxHeight = `${videoHeight}px`;
            }
        }

        handleResize();
        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    const startRecording = async () => {
        try {
            const constraints = { video: { width: 720, height: 1280 } };
            const newStream = await navigator.mediaDevices.getUserMedia(constraints);
            setStream(newStream);
            const mediaRecorder = new MediaRecorder(newStream);

            mediaRecorder.start();
            setIsRecording(true);

            mediaRecorderRef.current = mediaRecorder;
            mediaRecorder.ondataavailable = (event) => {
                recordedChunks.current.push(event.data);
            };

            mediaRecorder.onstop = () => {
                const blob = new Blob(recordedChunks.current, { type: 'video/mp4; codecs="avc1.42E01E, mp4a.40.2"' });
                const url = URL.createObjectURL(blob);
                console.log('Recorded video URL:', url);
                recordedChunks.current = [];
            };

            videoRef.current.srcObject = newStream;
            captureInterval.current = setInterval(captureImage, 5000); // capture img every 5 secs
        } catch (error) {
            console.error('Error accessing webcam:', error);
        }
    }

    function stopRecording() {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
            mediaRecorderRef.current.stop();
        }
        if (stream) {
            stream.getTracks().forEach((track) => track.stop());
            setStream(null);
            videoRef.current.srcObject = null;
        }
        if (captureInterval.current) {
            clearInterval(captureInterval.current);
        }
        setIsRecording(false);
        window.location.replace("https://www.roai.tech/") //TODO REPLACE URL AFTER TESTING!
    }

    // captures image (every 5 seconds) and sends to backend for processing
    function captureImage() {
        const canvas = canvasRef.current;
        const video = videoRef.current;
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageDataUrl = canvas.toDataURL('image/jpeg');
        console.log('Captured image:', imageDataUrl);
        const formData = new FormData();
        formData.append('image', imageDataUrl);

        ///fetch("https://example.com/upload", {
        ///    method: 'POST',
        ///    body: formData
        ///})
        ///    .then(response => {
        ///        if (response.ok) {
        ///            console.log('Image uploaded successfully.');
        ///        } else {
        ///            console.error('Failed to upload image:', response.statusText);
        ///        }
        ///    })
        ///    .catch(error => {
        ///        console.error('Error uploading image:', error);
        ///    });
    }

    return (
        <div>
            <div>
                {isRecording ? <video className="recording" ref={videoRef} autoPlay></video> : null}
            </div>
            <canvas ref={canvasRef} style={{ display: 'none' }}></canvas>
            <div>
                {isRecording ? (
                    <button className="button stop" onClick={stopRecording}>Stop Recording</button>
                ) :  (
                    <div className="container">
                        <h2 className="alignMiddle stack" style={{color:"white"}}>Not working?<span style={{fontWeight:"bold"}}>Check your phone!</span></h2>
                    </div>
                )}
            </div>
        </div>
    );
}

export default WebcamRecorder;