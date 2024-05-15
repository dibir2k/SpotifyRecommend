import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom'
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { useLocalStorage } from "@uidotdev/usehooks";
import { useNavigate } from "react-router-dom";
import { Loader } from "../utils";
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
  const navigate = useNavigate();
  const [trackData, saveTrackData] = useLocalStorage("trackData", []);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm({
    resolver: yupResolver(SignupSchema)
  });

  const onSubmit = async (data) => {
    setIsLoading(true);
    const requestOptions = {
      credentials: 'include',
      mode: 'cors',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'accepts': 'application/json',
        'Authorization': localStorage.getItem("id")
      },
      body: JSON.stringify(data)
    };
    let response = null;
    let jsonData = null;

    try {
      if (data.url) {
        response = await fetch('/api/recommendations/playlist', requestOptions);
      }
      else {
        response = await fetch('/api/recommendations/track', requestOptions);
      }

      jsonData = await response.json();

      saveTrackData(jsonData);

      setError(null);

      navigate('/tracks');
    }
    catch(error) { 
      setError(error);
      setIsLoading(false); 
    }
  }

  return (
    <div className='form-container'>
      {error !== null && !isLoading && <div>
        <p className='invalid-input'>Invalid Input. Please try again!</p>
      </div>}
      <form onSubmit={handleSubmit(onSubmit)}>
        {/* Conditionally render loading spinner */}
        {isLoading && <div><Loader /></div>}
        {!isLoading && (
          <>
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
          </>
        )}
      </form>
    </div>
  );
}

const LoggedOutHome = () => {
  return (
    <div className='home'>
    <div className="image-container">
       <img src="/imgs/Spotify_Logo.png" alt="Spotify Logo"></img>
    </div>
    <div> 
      <Link to='/login' className="button-sug">Log in</Link>
    </div>
    </div>
  )
}



const HomePage = ({logged}) => {
  // const [error, setError] = useState(null);
  // const [logged, setLogged] = useState(false);

  // useEffect(() => {
  //   const isLogged = localStorage.getItem("id") !== null;
  //   setLogged(isLogged);
    // const fetchLoggedStatus = async () => {
    //   try {
    //     console.log('Fetching logged status...');
    //     let id = localStorage.getItem("id");
    //     if (id == null) id = "None"
    //     // Fetch the authorization URL from the backend
    //     const response = await fetch('/api/logged', {
    //       credentials: 'include',
    //       mode: 'cors',
    //       method: 'GET',
    //       headers: { 'Content-Type': 'application/json', 
    //                 'Authorization': id},
    //     });
    //     if (!response.ok) {
    //       throw new Error('Failed to fetch logged status');
    //     }
    //     const data = await response.json();
    //     if (data.Authenticated) {
    //       setLogged(data.Authenticated);
    //       // localStorage.setItem("id", data.id);
    //     }
    //   } catch (error) {
    //     console.error('Logged error:', error);
    //     setError('Failed to check logged status. Please try again.');
    //   }
    // };
    // fetchLoggedStatus();
  // }, []);
  return (
    <div>
      {logged ? <LoggedInHome /> : <LoggedOutHome />}
    </div>
  )
}

export default HomePage