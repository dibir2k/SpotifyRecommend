import React from "react";
import { useState, useEffect } from "react";
import ListOfTracks from "../utils";
import Button from 'react-bootstrap/Button';
import { useLocalStorage } from "@uidotdev/usehooks";

const TopTracksPage = () => {
    const [topTracks, setTopTracks] = useState(null);
    const [trackData, saveTrackData] = useLocalStorage("topTrackData", []);
    const [error, setError] = useState(null);
    const [buttonClicked, setButtonClicked] = useState(false);
    const [buttonText, setButtonText] = useState("Recommendations");
    const id = localStorage.getItem("id");
    console.log(id)
    useEffect(() => {
        const fetchTopTracks = async () => {
          try {
            console.log('Fetching ...');
            // Fetch the authorization URL from the backend
            const response = await fetch('/api/recommendations/top-tracks-list', {
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
              setTopTracks(data);
              // localStorage.setItem("id", data.id);
            }
          } catch (error) {
            setError('Failed. Please try again.');
          }
        };
        fetchTopTracks();
      }, []);

      useEffect(() => {
        const fetchTrackData = async () => {
          try {
            // Fetch the authorization URL from the backend
            const response = await fetch('/api/recommendations/top-tracks', {
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
            setError('Failed. Please try again.');
          }
        };
        if (trackData == null || trackData.length == 0) {fetchTrackData()}
      }, []);

    const handleClick = () => {
        setButtonClicked(!buttonClicked);
        setButtonText("Top Tracks");
        console.log(buttonClicked);
    }
    if (topTracks == null) {
        return (
            <div>Getting your top tracks...</div>
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
                {!buttonClicked ? <ListOfTracks tracks={topTracks} /> : <ListOfTracks tracks={trackData} />}
            </div> 
            );
    }
}

export default TopTracksPage