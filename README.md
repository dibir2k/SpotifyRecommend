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

* **Flask** for the api development
* **Spotipy** to make requests to Spotify
* **Qdrant** vector database to store the collection of embedded vectors of each song, retrieve recommended tracks and upsert any new tracks to the database
* **Redis** to store the token information for each user so that authenticated endpoints in the api can be accessed

The vector database was first populated with roughly a million tracks from kaggle's dataset: "Spotify Million Song Dataset", available at: https://www.kaggle.com/datasets/notshrirang/spotify-million-song-dataset. The database grows as the user requests suggestions for tracks not present in the vector database yet. They are first added to the collection and later used to obtain recommendations of similar tracks.

### Frontend

The client side was built using React + Vite, and CSS.  

## Instructions for Running 

By following the steps below, you should be able to successfully run the app and try it on your local machine:

1. Clone the repository using 

```bash
git clone https://github.com/dibir2k/SpotifyRecommend.git
```

2. Navigate to the Cloned Repository: Change into the directory of the cloned repository.

```bash
cd <repository-directory>
```

3. Ensure that Git LFS is installed on the system where you've cloned the repository. 

```bash
git lfs version
```

If not, follow the steps in https://git-lfs.com.

4. Pull LFS Files: Run git lfs pull to download the large files tracked by Git LFS:

```bash
git lfs pull
```

5. After running git lfs pull, check that the CSV files and the contents of the qdrant_storage folder have been downloaded and are accessible in your local copy of the repository.

6. Login to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard). If necessary, read the latest [Developer Terms of Service](https://developer.spotify.com/terms) to complete your account set up.

    Create an app
    * An app provides the Client ID and Client Secret needed to request an access token by implementing any of the authorization flows. To create an app, go to your Dashboard, click on the Create an app button and enter the following information:

        - App Name: My App
        - App Description: This is my first Spotify app
        - Redirect URI: You won't need this parameter in this example, so use http://localhost:3000.
        - Finally, check the Developer Terms of Service checkbox and tap on the Create button.

7. After successfully creating the app, go to your app settings and copy your client id and client secret. Paste each of them in the corresponding place in the .env file.

8. Make sure you have Docker installed. Run the following command to build and start the docker container:

```bash
docker-compose up --build
```
9. After building is done, go to http://localhost:80 to start using the app.



