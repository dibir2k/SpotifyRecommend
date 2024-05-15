import React, { useEffect, useState } from "react";

import {
    // BrowserRouter as Router,
    Routes,
    Route
} from 'react-router-dom'
import HomePage from './Home';
import LoginPage from './Login';
import LogoutPage from './Logout';
import MyPlaylistsPage from './MyPlaylists';
import RecentlyPlayedPage from './RecentlyPlayed';
import TopTracksPage from './TopTracks';
import TracksPage from './Tracks';
import PlaylistPage from './Playlist';
import NavBar from "./Navbar";


const LoggedState = () => {
    const [logged, setLogged] = useState(false);

    useEffect(() => {
    const fetchLoggedStatus = async () => {
        try {
        let id = localStorage.getItem("id");
        if (id == null) id = "None";
        const response = await fetch('/api/logged', {
            credentials: 'include',
            mode: 'cors',
            method: 'GET',
            headers: { 'Content-Type': 'application/json', 'Authorization': id },
        });
        if (response.ok) {
            const data = await response.json();
            setLogged(data.Authenticated);
        }
        } catch (error) {
        console.error('Error during logged status check:', error);
        }
    };
    fetchLoggedStatus();
    }, []);

    return (
        <div>
        <NavBar logged={logged}/>
        <Routes>
            <Route path="/my-playlists" element={<MyPlaylistsPage/>}></Route>
            <Route path="/my-playlist/:playlist_id" element={<PlaylistPage />} />
            <Route path="/top-tracks" element={<TopTracksPage/>}></Route>
            <Route path="/recently-played" element={<RecentlyPlayedPage/>}></Route>
            <Route path="/tracks" element={<TracksPage/>}></Route>
            <Route path="/login" element={<LoginPage setLogged={setLogged}/>}></Route>
            <Route path="/logout" element={<LogoutPage/>}></Route>
            <Route path="/" element={<HomePage logged={logged}/>} />

        </Routes>
        </div>
    )
}

export default LoggedState;

