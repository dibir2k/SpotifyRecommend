import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom'
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";

const SignupSchema = yup.object().shape({
  trackName: yup.string().when("url", {
    is: (url) => url == "",
    then: schema => schema.required("Please provide a track name"),
    otherwise: schema => schema.optional(), 
  }),
  artistName: yup.string().when("url", {
    is: (url) => url == "",
    then: schema => schema.required("Please provide an artist name"),
    otherwise: schema => schema.optional(), 
  }),
  url: yup.string().url().when(["trackName", "artistName"], {
    is: (trackName, artistName) => trackName == "" && artistName == "",
    then: schema => schema.required("Please provide a url"),
    otherwise: schema => schema.optional(),
  })
}, [['trackName', 'url'], ['artistName', 'url']]);

const LoggedInHome = () => {
    const {
        register,
        handleSubmit,
        formState: { errors }
      } = useForm({
        resolver: yupResolver(SignupSchema)
      });
      const onSubmit = (data) => {
        alert(JSON.stringify(data));
      };

      return (
        <form onSubmit={handleSubmit(onSubmit)}>
          <div>
            <label>Track Name</label>
            <input {...register("trackName")} />
            {errors.trackName && <p>{errors.trackName.message}</p>}
          </div>
          <div style={{ marginBottom: 10 }}>
            <label>Artist Name</label>
            <input {...register("artistName")} />
            {errors.artistName && <p>{errors.artistName.message}</p>}
          </div>
          <div>
            <label>Playlist/Track url</label>
            <input {...register("url")} />
            {errors.url && <p>{errors.url.message}</p>}
          </div>
          <input type="submit" />
        </form>
      );
}

const LoggedOutHome = () => {
    return (
        <div className="home container">
            <h1 className="heading">Welcome to my Spotify Recommendation app</h1>
            <Link to='/login' className="btn btn-primary btn-lg">Log in to Spotify</Link>
        </div>
    )
}



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
                // localStorage.setItem("id", data.id);
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
        <div>
            {logged ? <LoggedInHome /> : <LoggedOutHome />}
        </div>
    )
}

export default HomePage