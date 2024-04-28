// import React, { useEffect, useState } from 'react';
// import { useNavigate, useLocation} from 'react-router-dom';
// import { Link } from 'react-router-dom';
// // const Login = () => {
// //   const [error, setError] = useState(null);
// //   const navigate = useNavigate(); // Access the navigate function using useNavigate hook

// //   useEffect(() => {
// //     const fetchAuthorizationUrl = async () => {
// //       try {
// //         console.log('Fetching authorization URL...');
        
// //         // Fetch the authorization URL from the backend
// //         const response = await fetch('/api/login', { credentials: 'include'});
// //         if (!response.ok) {
// //           throw new Error('Failed to fetch authorization URL');
// //         }
// //         const data = await response.json();
// //         console.log(data);
// //         console.log('Authorization URL received:', data.auth_url);

// //         // Redirect the user to the Spotify login page
// //         window.location.href = data.auth_url;
// //       } catch (error) {
// //         console.error('Login error:', error);
// //         setError('Failed to initiate login. Please try again.');
// //       }
// //     };

// //     console.log('Initiating login process...');
// //     fetchAuthorizationUrl();
// //   }, []);

// //   return (
// //     <div>
// //       {error && <p>{error}</p>}
// //       <h2>Redirecting to Spotify login...</h2>
// //     </div>
// //   );
// // };

// // export default Login;

// const LoginPage = () => {
//   const [loading, setLoading] = useState(true);
//   const navigate = useNavigate();
//   const location = useLocation();

//   useEffect(() => {
//     const fetchAuthUrl = async () => {
//       try {
//         const response = await fetch('/api/login', {
//             credentials: 'include',
//             mode: 'cors',
//             method: 'GET',
//             headers: { 'Content-Type': 'application/json' },
//           });
//         if (!response.ok) {
//           throw new Error('Failed to fetch authentication URL');
//         }
//         const data = await response.json();
//         if (data.Bearer) {
//             console.log(data.Bearer);
//             // Store the encrypted access token in localStorage or sessionStorage
//             localStorage.setItem('accessToken', data.Bearer);
//             console.log(localStorage.getItem('accessToken'))
//         }
//       } catch (error) {
//         console.error('Error fetching authentication URL:', error);
//         setLoading(false);
//       }
//     };

//     fetchAuthUrl();
//   }, []);

//   // useEffect(() => {
//   //   if (!loading) {
//   //     navigate('/');
//   //     return;

//   //   }
//   // }, [loading, navigate]);

//   if (loading) {
//     return <div>Loading...</div>;
//   }

//   return (
//     <div>
//       <h2>Login</h2>
//       {/* You can optionally display a loading indicator here */}
//     </div>
//   );
// };

// export default LoginPage;


// // const Login = () => {
// //     return (
// //       <div>
// //         <h1>Logging In...</h1>
// //         <Link to="http://127.0.0.1:5000/login">Login</Link> {"Click to login"}
// //       </div>
// //     );
// //   };
  
// //   export default Login;

// // const Login = () => {
// //     useEffect(() => {
// //         const redirectToLogin = async () => {
// //             try {
// //                 console.log('Redirecting to login page...');
// //                 const response = await fetch('/login', {
// //                     method: 'GET',
// //                     credentials: 'include', // Include credentials for CORS
// //                     headers: {
// //                         'Content-Type': 'application/json'
// //                     }
// //                 });
// //                 if (!response.ok) {
// //                     throw new Error('Failed to redirect to login page');
// //                 }
// //             } catch (error) {
// //                 console.error('Error redirecting to login page:', error);
// //                 // Handle error (e.g., display error message)
// //             }
// //         };

// //         redirectToLogin();
// //     }, []);

// //     return (
// //         <div>
// //             {/* You can optionally display a loading spinner or message here */}
// //             Redirecting to login page...
// //         </div>
// //     );
// // };

// // export default Login

import React, { useEffect } from "react";

const Login = () => {
  useEffect(() => {
    const handleLogin = async () => {
      try {
        const response = await fetch("/api/authurl");
        const data = await response.json();
        const codeUrl = data.AuthUrl;
        console.log(codeUrl);
        
        // Redirect to the GitHub login page
        window.location.replace(codeUrl);

        // Check if the URL contains the authorization code
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get("code");
        
        if (code) {
          // If the authorization code is present, make a request to your backend to exchange it for an access token
          const response = await fetch(`/api/login?code=${code}`);
          const data = await response.json();

          // Assuming your backend responds with a token
          const accessToken = data.Bearer;

          // Store the token in localStorage or sessionStorage for future use
          localStorage.setItem("accessToken", accessToken);

          // Redirect to the desired page after successful login
          window.location.replace("http://localhost:5173");
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

export default Login;
