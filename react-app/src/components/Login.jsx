// import React, { useEffect, useState } from 'react';
// import { useNavigate, useLocation} from 'react-router-dom';
// import { Link } from 'react-router-dom';
// // const Login = () => {
// //   const [error, setError] = useState(null);
// //   const navigate = useNavigate(); // Access the navigate function using useNavigate hook

// import React, { useEffect } from 'react';

// const LoginPage = () => {
//     useEffect(() => {
//         const handleLogin = async () => {
//             try {
//                 // Fetch the authentication URL from the backend
//                 const response = await fetch('/api/login');
//                 const data = await response.json();
//                 console.log(data);
//                 if (data.AuthUrl) {
//                     // Handle the redirect URL from the backend
//                     window.open(data.AuthUrl, "_self");
//                 } else {
//                     console.error('Failed to fetch authentication URL');
//                 }
//             } catch (error) {
//                 console.error('Error during login:', error);
//             }
//         };

//         const fetchToken = async () => {
//           try {
//             // Fetch the access token from your Flask backend
//             const response = await fetch('/api/token');
//             const data = await response.json();
      
//             // Store the access token in localStorage or state
//             localStorage.setItem('accessToken', data.Bearer);
      
//             // Redirect the user to the homepage or another route
//             window.location.href = '/'; // Replace '/' with the desired route
//           } catch (error) {
//             console.error('Error fetching token:', error);
//           }
//         };

//         // Call the handleLogin function when the component mounts
//         handleLogin();
//         fetchToken();
//     }, []);

//     return (
//         <div>
//             {/* Optionally, you can display a loading spinner or message here */}
//             Redirecting to login page...
//         </div>
//     );
// };

// export default LoginPage;


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

// import React, { useEffect } from "react";

// const Login = () => {
//   useEffect(() => {
//     const handleLogin = async () => {
//       try {
//         const response = await fetch("/api/authurl");
//         const data = await response.json();
//         const codeUrl = data.AuthUrl;
//         console.log(codeUrl);
//         // Redirect to the Spotify login page
//         window.location.href = codeUrl;

//         // Check if the URL contains the authorization code
//         const urlParams = new URLSearchParams(window.location.search);
//         const code = urlParams.get("code");

//         if (code) {
//           // If the authorization code is present, make a request to your backend to exchange it for an access token
//           const response = await fetch(`/api/login?code=${code}`);
//           const data = await response.json();

//           // Assuming your backend responds with a token
//           const accessToken = data.Bearer;

//           // Store the token in localStorage or sessionStorage for future use
//           localStorage.setItem("accessToken", accessToken);

//           // Redirect to the desired page after successful login
//           window.location.replace("http://localhost:5173");
//         }
//       } catch (error) {
//         console.error("Error during login:", error);
//       }
//     };

//     // Call the handleLogin function when the component mounts
//     handleLogin();
//   }, []);

//   return (<div>
//                  {/* You can optionally display a loading spinner or message here */}
//                  Redirecting to login page...
//          </div>); // No UI elements to render
// };

// export default Login;


// class Login extends React.Component{
//   constructor(props){
//       super(props);       
//       this.getCodeFromSpotify = this.getCodeFromSpotify.bind(this);         
//   }

//   async getCodeFromSpotify(e){
//     try {        
//       const response = await fetch("/api/authurl");
//       const data = await response.json();
//       const codeUrl = data.AuthUrl;
//       window.location.replace(codeUrl);
//     }
//     catch(error) {
//       console.error("Error during login:", error);
//     }
//   }


//   componentDidMount(){
//       let cUrl = window.location.href;
//       if(cUrl.includes("code=")){            
//           let code = cUrl.split("code=")[1];                              
//           fetch('/api/login?code=' + code)
//               .then((resp) => resp.json())
//               .then((resp) => {                
//                   if(resp.Bearer){
//                       localStorage.setItem("accessToken", resp.Bearer);                           
//                       window.location.replace("http://localhost:5173");
//                       return true;               
//                   }                    
//               })
//               .catch((e) => {
//                   // handle when something goes wrong with your authentication
//                   console.error("Error during login:", e);
//               })
//       }           
//   }

//   render(){       
//       return [            
//           <div className="row">
//               <div className="col-sm-12 text-center">                    
//                   <div className="row justify-content-center">
//                       <a onClick={(e) => {this.getCodeFromSpotify(e)}}  className="btn btn-primary">
//                           Sign in with Spotify
//                       </a>
//                   </div>
//               </div>
//           </div>            
//       ];
//   }
// }

// export default Login;



import React, { useEffect, useState } from "react";

const LoginPage = () => {

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
          window.location.replace("http://localhost:5173");
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