// // import {createAuthProvider} from 'react-token-auth'

// // export const [useAuth, authFetch, login, logout] =
// //     createAuthProvider({
// //         accessTokenKey: 'access_token',
// //         onUpdateToken: (token) => fetch('/refresh', {
// //             method: 'POST',
// //             body: token.refresh_token
// //         })
// //         .then(r => r.json())
// //     })

// import { createAuthProvider } from 'react-token-auth';

// // type Session = { accessToken: string; refreshToken: string };

// export const { useAuth, authFetch, login, logout } = createAuthProvider({
//     getAccessToken: session => session.access_token,
//     storage: localStorage,
//     onUpdateToken: token =>
//         fetch('/refresh', {
//             method: 'POST',
//             body: token.refresh_token,
//         }).then(r => r.json()),
// });



import { createAuthProvider } from 'react-token-auth';

export const { useAuth, authFetch, login, logout } = createAuthProvider({
    getAccessToken: session => session.access_token,
    storage: localStorage,
    onUpdateToken: async token => {
        try {
            const response = await fetch('/refresh', {
                method: 'POST',
                body: JSON.stringify({ refresh_token: token.refresh_token }),
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            return data.access_token; // Return the new access token
        } catch (error) {
            console.error('Error refreshing access token:', error);
            throw error; // Throw the error to be caught by the calling code
        }
    },
});