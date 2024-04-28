import React, { useEffect, useState } from 'react';
import { useAuth } from '../auth'


const HomePage = () => {
    const [error, setError] = useState(null);
    const [logged, setLogged] = useState(false);

    useEffect(() => {
        const fetchLoggedStatus = async () => {
        try {
            console.log('Fetching logged status...');
            
            // Fetch the authorization URL from the backend
            const response = await fetch('/api/logged', {
                credentials: 'include',
                mode: 'cors',
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
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
    });
        return (
            <div className="home">
                <h1>Home Page</h1>
                <p>{ logged? "Yes" : "No"}</p>
            </div>
        )
    }

export default HomePage

// const LoggedOutHome = () => {
//     return (
//         <div className="home container">
//             <h1 className="heading">Welcome to my Spotify Recommendation app</h1>
//             <Link to='/login' className="btn btn-primary btn-lg">Log in to Spotify</Link>
//         </div>
//     )
// }

// const HomePage = () => {

//     const [logged] = useAuth()

//     return (
//         <div>
//             {logged ? <LoggedinHome /> : <LoggedOutHome />}
//         </div>
//     )
// }

// export default HomePage