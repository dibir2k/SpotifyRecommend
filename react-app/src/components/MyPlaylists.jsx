import React, { useEffect, useState } from "react";

const MyPlaylistsPage = () => {
    const [playlists, setPlaylists] = useState();
    const id = localStorage.getItem("id");
    useEffect(() => {
        const fetchPlaylists = async () => {
            try {
                const response = await fetch('/api//recommendations/my-playlists', {
                    credentials: 'include',
                    mode: 'cors',
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json', 
                              'Authorization': id},
                  })
                
                const data = await response.json();

                setPlaylists(data);

                console.log(data)
            
            }
            catch (error) {
                console.log(error)

            }
        }
        fetchPlaylists();
    }, [])

    return (
        <div className="MyPlaylists">
            <h1>My Playlists</h1>
        </div>
    )
}

export default MyPlaylistsPage