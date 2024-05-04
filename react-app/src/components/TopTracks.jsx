import React from "react";
import { useState, useEffect } from "react";
import ListOfTracks from "../utils";
import Button from 'react-bootstrap/Button';
import { useNavigate } from "react-router-dom";

const TopTracksPage = () => {
    const [topTracks, setTopTracks] = useState(null);
    const [trackData, setTrackData] = useState(null);
    const [error, setError] = useState(null);
    const [buttonClicked, setButtonClicked] = useState(null);
    const navigate = useNavigate();
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
            if (data) {
              setTrackData(data);
              localStorage.setItem("topTracksData", data);
            }
          } catch (error) {
            setError('Failed. Please try again.');
          }
        };
        fetchTrackData();
      }, []);

    const handleClick = () => setButtonClicked(true);
    return ( 
        <div>
            <Button 
                onClick={() => trackData !== null ? handleClick : null}
                variant="success" 
                size="lg" 
                disabled = {trackData == null}>
                Recommendations
            </Button>
            {topTracks !== null && !buttonClicked ? <ListOfTracks tracks={topTracks} /> : <ListOfTracks tracks={trackData} />}
        </div> 
        );
}

export default TopTracksPage