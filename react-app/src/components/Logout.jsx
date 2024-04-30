import React, { useEffect } from "react";

const LogoutPage = () => {
    useEffect(() => {
        const handleLogout = async () => {
          try {
            const response = await fetch('/api/logout', {
                method: 'POST',
                headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id: localStorage.getItem("id")}),
            });
            const data = await response.json();
            console.log(data);
            localStorage.removeItem("accessToken");
            localStorage.removeItem("id");
            window.location.href = "/";
          } catch (error) {
            console.error("Error during logout:", error);
          }
        };
    
        // Call the handleLogin function when the component mounts
        handleLogout();
      }, []);
    
      return (<div>
                     {/* You can optionally display a loading spinner or message here */}
                     Redirecting to home page...
             </div>); // No UI elements to render
    };

export default LogoutPage