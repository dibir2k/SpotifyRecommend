import React from 'react'
import { Link } from 'react-router-dom'
import { useState, useEffect} from 'react'
import { Popup } from 'reactjs-popup';



const LoggedInLinks = () => {
    return (
        <>
            <li className="nav-item">
                <Link className="nav-link active" to="/">Home</Link>
            </li>
            <li className="nav-item">
                <Link className="nav-link  active" to="/my-playlists">My Playlists</Link>
            </li>
            <li className="nav-item">
                <Link className="nav-link  active" to="/top-tracks">Top Tracks</Link>
            </li>
            <li className="nav-item">
                <Link className="nav-link  active" to="/recently-played">Recently Played</Link>
            </li>
            <li className="nav-item">
                <Link className="nav-link active" to="/logout" >Logout</Link>
            </li>
        </>
    )
}


const LoggedOutLinks = () => {

    return (
        <>
            <li className="nav-item">
                <Link className="nav-link active" to="/">Home</Link>
            </li>
            <li className="nav-item">
                <Link className="nav-link active" to="/login" >Login</Link>
            </li>
        </>
    )
}

const NavBar = () => {

    const [logged, setLogged] = useState(false);
    const [error, setError] = useState(null);
    console.log(logged)

    useEffect(() => {
        const fetchLoggedStatus = async () => {
        try {
            console.log('Fetching logged status...');
            let id = localStorage.getItem("id");
            if (id == null) id = "None"
            // Fetch the authorization URL from the backend
            const response = await fetch('/api/logged', {
            credentials: 'include',
            mode: 'cors',
            method: 'GET',
            headers: { 'Content-Type': 'application/json', 
                        'Authorization': id},
            });
            if (!response.ok) {
            throw new Error('Failed to fetch logged status');
            }
            const data = await response.json();
            if (data.Authenticated) {
                setLogged(data.Authenticated);
            }
            console.log(data);
        } catch (error) {
            console.error('Logged error:', error);
            setError('Failed to check logged status. Please try again.');
        }
        };
        fetchLoggedStatus();
    }, []);

    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <div className="container-fluid">
                <Link className="navbar-brand" to="/">Spotify</Link>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav">
                        {logged?<LoggedInLinks/>:<LoggedOutLinks/>}
                    </ul>
                </div>
            </div>
        </nav>
    )
}

export default NavBar