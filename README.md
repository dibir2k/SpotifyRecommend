# Spotify Music Recommendation App

## Project Description

This is a web application for getting song recommendations. Using this app, you can get suggestions of similar songs according to:

* A particular track
* A public playlist available on Spotify
* Any of the user's playlists
* The user's recently played tracks on Spotify
* The user's top tracks according to Spotify

### Backend 
The backend was built using the following libraries and services: 

* Flask for the api development
* Spotipy to make requests to Spotify
* Qdrant vector database to store the collection of embedded vectors of each song, retrieve recommended tracks and upsert any new tracks to the database
* Redis to store the token information for each user so that authenticated endpoints in the api can be accessed

The vector database was first populated with roughly a million tracks from kaggle's dataset: "Spotify Million Song Dataset", available at: https://www.kaggle.com/datasets/notshrirang/spotify-million-song-dataset. The database grows as the user requests suggestions for tracks not present in the vector database yet. They are first added to the collection and later used to obtain recommendations of similar tracks.

### Frontend
The clinet side was built using React + Vite, and CSS.  

## Instructions for Running the app

