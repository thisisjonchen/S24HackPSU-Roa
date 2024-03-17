import WebcamRecorder from "../components/recorder";
import {useEffect, useRef} from "react";
import LocationTracker from "../components/location";

function Record() {
    const videoRef = useRef(null);
    const loadingRef = useRef(null);

    useEffect(() => {
        if (videoRef.current && loadingRef.current) {
            videoRef.current.style.display = 'none';
            loadingRef.current.style.display = 'block';

            const timer = setTimeout(() => {
                videoRef.current.style.display = 'block';
                loadingRef.current.style.display = 'none';
            }, 2000);

            return () => clearTimeout(timer);
        }
    }, []);


    return (
        <div className="container alignMiddle" style={{height:"100vh"}}>
            <div className="">

            </div>
            <div id="video" className="videoContainer alignMiddle">
                <div ref={loadingRef} id="loading"></div>
                <div ref={videoRef} id="video" style={{overflow:"hidden"}}>
                    <WebcamRecorder/>
                    <LocationTracker/>
                </div>
            </div>
        </div>
    );
}

export default Record