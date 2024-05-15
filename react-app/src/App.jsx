import { useState } from 'react'
import './App.css'
import './styles/main.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react'
import ReactDOM from 'react-dom'
import NavBar from './components/Navbar';

import {
    BrowserRouter as Router,
    Routes,
    // Route
} from 'react-router-dom'
// import HomePage from './components/Home';
// import LoginPage from './components/Login';
// import LogoutPage from './components/Logout';
// import MyPlaylistsPage from './components/MyPlaylists';
// import RecentlyPlayedPage from './components/RecentlyPlayed';
// import TopTracksPage from './components/TopTracks';
// import TracksPage from './components/Tracks';
// import PlaylistPage from './components/Playlist';
import LoggedState from './components/LoggedState';
const App=()=>{

    
    return (
        <Router>
        <div className="">
            <LoggedState>
                {/* <NavBar/>
                <Routes>
                    <Route path="/my-playlists" element={<MyPlaylistsPage/>}></Route>
                    <Route path="/my-playlist/:playlist_id" element={<PlaylistPage />} />
                    <Route path="/top-tracks" element={<TopTracksPage/>}></Route>
                    <Route path="/recently-played" element={<RecentlyPlayedPage/>}></Route>
                    <Route path="/tracks" element={<TracksPage/>}></Route>
                    <Route path="/login" element={<LoginPage/>}></Route>
                    <Route path="/logout" element={<LogoutPage/>}></Route>
                    <Route path="/" element={<HomePage />} />

                </Routes> */}
            </LoggedState>
        </div>
        </Router>
    )
}

export default App
