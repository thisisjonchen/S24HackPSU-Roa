import {useEffect, useState} from 'react';

 function LocationTracker() {
     const [location, setLocation] = useState(null);
     useEffect(() => {
         const intervalId = setInterval(() => {
             navigator.geolocation.getCurrentPosition(
                 (position) => {
                     setLocation({
                         latitude: position.coords.latitude,
                         longitude: position.coords.longitude,
                     });
                     console.log(position.coords.longitude, position.coords.latitude)
                 },
                 (error) => console.error(error),
                 { enableHighAccuracy: true }
             );
         }, 5000);

         return () => clearInterval(intervalId);
     }, []);


     //useEffect(() => {
    //    const intervalId = setInterval(() => {
    //        navigator.geolocation.getCurrentPosition(
    //            // captures location (synced every 5 seconds) and sends to backend for processing
    //            (position) => {
    //                ///fetch(
    //                ///    `API`,
    //                ///    {
    //                ///        method: "PUT",
    //                ///        body: JSON.stringify({latitude: position.coords.latitude, longitude: position.coords.longitude}),
    //                ///        headers: {
    //                ///            "Content-Type": "application/json",
    //                ///            "Access-Control-Allow-Origin": "*"
    //                ///        },
    //                ///    },
    //                ///).then()
    //            },
    //            (error) => console.error(error),
    //            { enableHighAccuracy: true }
    //        );
    //    }, 5000);
}

export default LocationTracker;
