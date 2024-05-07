import React from "react";
import { useState, useEffect } from "react";
import ListOfTracks from "../utils";
import Button from 'react-bootstrap/Button';
import { useLocalStorage } from "@uidotdev/usehooks";

const RecentlyPlayedPage = () => {
    const [rpTracks, setRpTracks] = useState(null);
    const [trackData, saveTrackData] = useLocalStorage("rpTrackData", []);
    const [buttonClicked, setButtonClicked] = useState(false);
    const [buttonText, setButtonText] = useState("Recommendations");
    const id = localStorage.getItem("id");

    useEffect(() => {
        const fetchRpTracks = async () => {
          try {
            console.log('Fetching ...');
            // Fetch the authorization URL from the backend
            const response = await fetch('/api/recommendations/recently-played-list', {
              credentials: 'include',
              mode: 'cors',
              method: 'GET',
              headers: { 'Content-Type': 'application/json', 
                        'Authorization': id},
            });
            if (!response.ok) {
              throw new Error('Failed to fetch top tracks');
            }
            const data = await response.json();
            console.log(data);
            if (data) {
              setRpTracks(data);
              // localStorage.setItem("id", data.id);
            }
          } catch (error) {
            console.log(error);
          }
        };
        fetchRpTracks();
      }, []);

      useEffect(() => {
        const fetchRpTrackData = async () => {
          try {
            // Fetch the authorization URL from the backend
            const response = await fetch('/api/recommendations/recently-played', {
              credentials: 'include',
              mode: 'cors',
              method: 'GET',
              headers: { 'Content-Type': 'application/json', 
                        'Authorization': id},
            });
            if (!response.ok) {
              throw new Error('Failed to fetch suggestions for top tracks');
            }
            const data = await response.json();
            console.log(data);
            if (data) {
              saveTrackData(data);
            }
          } catch (error) {
            console.log(error);
          }
        };
        if (trackData == null || trackData.length == 0) {fetchRpTrackData()}
      }, []);

    const handleClick = () => {
        setButtonClicked(!buttonClicked);
        setButtonText("Recently Played");
        console.log(buttonClicked);
    }
    if (rpTracks == null) {
        return (
            <div>Getting your recently played tracks...</div>
        )
    }
    else {
        return ( 
            <div>
                <Button 
                    onClick={trackData.length > 0 ? handleClick : null}
                    variant="success" 
                    size="lg" 
                    disabled={trackData == null || trackData.length == 0}
                    > {buttonText}
                </Button>
                {!buttonClicked ? <ListOfTracks tracks={rpTracks} /> : <ListOfTracks tracks={trackData} />}
            </div> 
            );
    }
}

export default RecentlyPlayedPage