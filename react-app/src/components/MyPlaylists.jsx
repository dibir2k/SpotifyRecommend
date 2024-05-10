import React, { useEffect, useState } from "react";
import { ListOfTracks, Loader } from "../utils";
import { useNavigate } from "react-router-dom"

const MyPlaylistsPage = () => {
    const [playlists, setPlaylists] = useState([]);
    const id = localStorage.getItem("id");
    const navigate = useNavigate();
    useEffect(() => {
        const fetchPlaylists = async () => {
            try {
                const response = await fetch('/api/recommendations/my-playlists', {
                    credentials: 'include',
                    mode: 'cors',
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json', 
                              'Authorization': id},
                  })
                
                const data = await response.json();

                setPlaylists(data);

                console.log(data);
            }
            catch (error) {
                console.log(error);
            }
        }
        fetchPlaylists();
    }, [])

    const handleClick = (playlist_id) => {
        navigate(`/my-playlist/${playlist_id}`);
    }

    if (playlists == null || playlists.length == 0) {
        return (
            <div><Loader /></div>
        )
    }
    else {
        return (
            <div className="playlist-grid">
            {playlists.map(playlist => (
                <div key={playlist.playlist_id} className="playlist-item" onClick={() => handleClick(playlist.playlist_id)}>
                <img src={playlist.image_url} alt={playlist.name} />
                <p className="playlist-name">{playlist.playlist_name}</p>
                </div>
            ))}
            </div>
        );
    }
}

export default MyPlaylistsPage