import React, { useEffect, useState } from 'react';
import { useLocalStorage } from "@uidotdev/usehooks";
import { useParams } from 'react-router-dom';
import { ListOfTracks, Loader } from "../utils";

const PlaylistPage = () => {
    const { playlist_id } = useParams();
    const [playlistData, setPlaylistData] = useState([]);
    const [recommendData, saveRecommendData] = useLocalStorage(`data-${playlist_id}`, []);
    const [error, setError] = useState(null);
    const id = localStorage.getItem("id");
    const [buttonText, setButtonText] = useState("Recommendations");
    const [buttonClicked, setButtonClicked] = useState(false);

  useEffect(() => {
    const fetchPlaylistData = async () => {
        console.log(playlist_id)
        try {
            const response = await fetch('/api/recommendations/playlist/playlist-data', {
                credentials: 'include',
                mode: 'cors',
                method: 'GET',
                headers: { 'Content-Type': 'application/json', 
                        'Authorization': id, 
                        'Playlist-id': playlist_id},
            })
            
            const data = await response.json();
        
            setPlaylistData(data);
        }
        catch (error) {
            console.log(error)
        }
    }
    fetchPlaylistData();
  }, [playlist_id]);

  useEffect(() => {
    const fetchRecommendData = async () => {
      try {
        // Fetch the authorization URL from the backend
        const response = await fetch(`/api/recommendations/playlist/${playlist_id}`, {
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
          saveRecommendData(data);
        }
      } catch (error) {
        setError(error);
      }
    };
    if (recommendData == null || recommendData.length == 0) {fetchRecommendData()}
  }, []);

  const handleClick = () => {
    setButtonClicked(!buttonClicked);
    if (buttonText == "Recommendations") setButtonText("Playlist Tracks");
    else setButtonText("Recommendations");
    console.log(buttonClicked);
}

  if (playlistData == null || playlistData.length == 0) {
    return (
        <div><Loader /></div>
    )
}
else {
    return ( 
        <div className="custom-container">
            <button className="button-sug"
                onClick={recommendData.length > 0 ? handleClick : null}
                //variant="success" 
                size="lg" 
                disabled={recommendData == null || recommendData.length == 0}
                > {buttonText}
            </button>
            {!buttonClicked ? <ListOfTracks tracks={playlistData} /> : <ListOfTracks tracks={recommendData} />}
        </div> 
        );
}
}

export default PlaylistPage;