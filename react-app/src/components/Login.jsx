import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"

const LoginPage = () => {
  const navigate = useNavigate();
  useEffect(() => {
    const handleLogin = async () => {
      try {
        // Check if the URL contains the authorization code
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get("code");
        console.log(code);
        
        if (code) {
          // If the authorization code is present, make a request to your backend to exchange it for an access token
          const response = await fetch(`/api/login?code=${code}`, {
            credentials: 'include',
            mode: 'cors',
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
          });
          console.log(response);
          if (response.ok) {
            const data = await response.json();

            // Assuming your backend responds with a token
            const id = data.id;

            // Store the token in localStorage or sessionStorage for future use
            localStorage.setItem("id", id);
          }

          // Redirect to the desired page after successful login
          // window.location.replace("http://localhost:4173");
          navigate('/');
        }
        else {
          const response = await fetch("/api/authurl");
          const data = await response.json();
          const codeUrl = data.AuthUrl;
          console.log(codeUrl);
          
          // Redirect to the GitHub login page
          window.location.replace(codeUrl);
        }
      } catch (error) {
        console.error("Error during login:", error);
      }
    };

    // Call the handleLogin function when the component mounts
    handleLogin();
  }, []);

  return (<div>
                 {/* You can optionally display a loading spinner or message here */}
                 Redirecting to login page...
         </div>); // No UI elements to render
};

export default LoginPage;