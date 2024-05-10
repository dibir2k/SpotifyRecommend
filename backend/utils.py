import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from qdrant_client import QdrantClient, models
import json
import os
import glob
import requests

DIR = os.getcwd()

def read_df():
    df = pd.read_csv(DIR + "/spotify_data.csv")
    df.drop(df.columns[0], axis=1, inplace=True)

    return df

# clean data frame
def clean_df(df):
    # Adter checking, we see that the artist with missing values is called "None" and the only track without name is called "None", 
    # so we can substitue all those values by the string "None"
    df = df.fillna("None", inplace=False)

    # Drop unnecessary columns
    features_df = df.drop(["artist_name", "year", "track_id", "track_name", "duration_ms", "key", "time_signature", "popularity"], axis=1)

    all_genres_dict = features_df["genre"].value_counts().to_dict()
    # Use this function to search for any files which match your filename
    files_present = glob.glob("./features.csv")


    # if no matching files, write to csv, if there are matching files, print statement
    if not files_present:
        features_df.to_csv("./features.csv")

    return features_df

# Get genre of an artist

def get_artist_genres(sp, artist_name):
    result = sp.search(artist_name)
    track = result['tracks']['items'][0]
    artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
    return artist["genres"]


# Get main genre from list of genres

def get_main_genre(spotify_df, genres_list):
    all_genres_dict = spotify_df["genre"].value_counts().to_dict()
    tracks_genres = []
    for genres in genres_list:
        if len(genres) == 0: 
            tracks_genres.append("none")
            continue

        champion_genre = "none"
        current_count = 0
        for genre in genres:
            if genre in all_genres_dict.keys():
                new_count = all_genres_dict[genre]
                if new_count > current_count:
                    champion_genre = genre
                    current_count = new_count

        tracks_genres.append(champion_genre)
    
    return tracks_genres


# get track uri from track and artist name

def get_track_uri(sp, track_name, artist_name):
    query = f"artist:{artist_name} track:{track_name}"
    results = sp.search(q=query, type='track')
    if results['tracks']['total'] > 0:
        track_uri = results['tracks']['items'][0]['uri']
        artist_genre = [get_artist_genres(sp, artist_name)]
        return track_uri, artist_genre
    else:
        return None


def get_recently_played_list(sp):
    payload = []
    #if token:
    results = sp.current_user_recently_played(limit = 50)
    recently_items = results['items']

    for item in recently_items:
        uri = item['track']['uri']
        artist_name = item['track']['artists'][0]['name']
        track_name = item['track']['name']
        payload.append({"artist_name": artist_name, "track_name": track_name, "track_id": uri})

    track_ids = [pld["track_id"] for pld in payload]
    images_url, albums_name, durations = get_album_images(sp, track_ids)

    for i, pld in enumerate(payload):
        pld["image"] = images_url[i]
        pld["album_name"] = albums_name[i]
        pld["duration"] = durations[i]

    return payload

def get_recently_played(sp):
    uris = []
    genres = []
    payload = []
    #if token:
    results = sp.current_user_recently_played(limit = 25)
    recently_items = results['items']

    for item in recently_items:
        uri = item['track']['uri']
        uris.append(item['track']['uri'])
        artist_name = item['track']['artists'][0]['name']
        track_name = item['track']['name']
        artist_genres = get_artist_genres(sp, artist_name)
        genres.append(artist_genres)
        payload.append({"artist_name": artist_name, "track_name": track_name, "track_id": uri})

    return uris, genres, payload
    #else:
    #    print("Can't get token")

def get_top_tracks_list(sp):
    payload = []

    results = sp.current_user_top_tracks(limit=50)
    top_tracks_items = results['items']
    results = sp.next(results)
    top_tracks_items.extend(results['items'])
    for item in top_tracks_items:
        artist_name = item['artists'][0]['name']
        track_name = item['name']
        payload.append({"artist_name": artist_name, "track_name": track_name, "track_id": item['uri']})

    track_ids = [pld["track_id"] for pld in payload]
    images_url, albums_name, durations = get_album_images(sp, track_ids)

    for i, pld in enumerate(payload):
        pld["image"] = images_url[i]
        pld["album_name"] = albums_name[i]
        pld["duration"] = durations[i]

    return payload

def get_top_tracks(sp):
    uris = []
    genres = []
    payload = []
    
    results = sp.current_user_top_tracks(limit=25)
    top_tracks_items = results['items']
    for item in top_tracks_items:
        uris.append(item['uri'])
        artist_name = item['artists'][0]['name']
        track_name = item['name']
        genres.append(get_artist_genres(sp, artist_name))
        payload.append({"artist_name": artist_name, "track_name": track_name, "track_id": item['uri']})

    return uris, genres, payload
    #else:
    #    print("Can't get token for")

# Get tracks uris in a playlist

def get_playlist_tracks(sp, username, playlist_id):
    # Ref - https://stackoverflow.com/questions/39086287/spotipy-how-to-read-more-than-100-tracks-from-a-playlist?noredirect=1&lq=1
    #if token:
    payload = []
    results = sp.user_playlist_tracks(username,playlist_id)
    playlist_items = results['items']
    uris = []
    genres = []
    while results['next']:
        results = sp.next(results)
        playlist_items.append(results['items'])

    for item in playlist_items:
        is_local = item["is_local"]
        if is_local == True: # Filtering out any local tracks (i.e. not hosted by Spotify)
            continue
        else:
            track_uri = item["track"]["uri"]
            track_artist = item["track"]["artists"][0]["name"]
            track_name = item["track"]["name"]
            genres.append(get_artist_genres(sp, track_artist))
            payload.append({"artist_name": track_artist, "track_name": track_name, "track_id": track_uri})

            uris.append(track_uri)
    return uris, genres, payload
    #else:
    #    print("Can't get token for ", username)


# Get features of song or list of songs in a playlist as a data frame

def get_song_features(sp, spotify_df, track_name=None, artist_name=None, username=None): 
    tracks = []
    genres = []
    payload = []

    if  "/track" in track_name:
        track = sp.track(track_name)
        artist_name = track["artists"][0]["name"]
        genres_list = [get_artist_genres(sp, artist_name)]
        genre = get_main_genre(spotify_df, genres_list)
        tracks = [track_name]
        name_track = track["name"]
        track_id = track["id"]
        payload.append({"artist_name": artist_name, "track_name": name_track, "track_id": track_id})

    elif artist_name != None:
        track_uri, genres = get_track_uri(sp, track_name, artist_name)
        tracks = [track_uri]
        genre = get_main_genre(spotify_df, genres)
        payload.append({"artist_name": artist_name, "track_name": track_name, "track_id": track_uri})
    else:
        tracks, genres, payload = get_playlist_tracks(sp, username, track_name)
        genre = get_main_genre(spotify_df, genres)

    return tracks, genre, payload

def create_df_tracks(sp, tracks, genre):
    dict_features = sp.audio_features(tracks)
    df_tracks = pd.DataFrame(dict_features)

     # Drop unnecessary columns
    df_tracks = df_tracks.drop(["type", "id", "uri", "duration_ms", "key", "time_signature", "analysis_url", "track_href"], axis=1)
    df_tracks["genre"] = genre

    return df_tracks


# # Extract features

# def get_all_features(df, track_df=None):
#     df_columns = list(df.columns)
#     track_df = track_df[list(df_columns)]
    
#     len_track_df = len(track_df)
#     df = pd.concat([df, track_df], ignore_index=True)
    
#     #Encode genre in one-hot sense
#     total_df = pd.get_dummies(df, columns=["genre"], dtype="int64")

#     for col in total_df.columns:
#         if total_df[col].dtype == "float64":
#             total_df[col] = (total_df[col] - total_df[col].mean()) / total_df[col].std()
    
#     df  = total_df.head(len(df) - len_track_df)
#     track_df  = total_df.tail(len_track_df)

#     return df.to_numpy(), track_df.to_numpy()



def get_features(track_df=None):
    df = pd.read_csv("./features.csv")
    df.drop(df.columns[0], axis=1, inplace=True)

    df_columns = list(df.columns)
    track_df = track_df[list(df_columns)]
    
    len_track_df = len(track_df)
    total_df = pd.concat([df, track_df], ignore_index=True)
    total_df = total_df[~total_df.duplicated(keep='last')]

    total_df.to_csv("./features.csv")
    
    #Encode genre in one-hot sense
    features_df = pd.get_dummies(total_df, columns=["genre"], dtype="int64").tail(len_track_df)

    features_df = features_df.drop(['genre_none'], axis=1, errors='ignore')

    for col in df.columns:
        if df[col].dtype == "float64":
            features_df[col] = (features_df[col] - df[col].mean()) / df[col].std()
    

    return features_df.to_numpy()

def ms_to_string(duration_ms):
    millis = int(duration_ms)
    seconds=(millis/1000)%60
    seconds = int(seconds)
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)

    if seconds <= 9: return f"{minutes}:0{seconds}"
    else: return f"{minutes}:{seconds}"

def get_album_images(sp, track_ids):
    images_url = []
    albums_name = []
    durations = []
    n_tracks = len(track_ids)
    for i in range(0, n_tracks, 50):
        left_limit = i
        right_limit = min(i + 50, n_tracks)
        tracks = sp.tracks(track_ids[left_limit:right_limit])["tracks"]
        for track in tracks:
            images_url.append(track["album"]["images"][2]["url"])
            albums_name.append(track["album"]["name"]) 
            duration = track["duration_ms"]
            durations.append(ms_to_string(duration))

    return images_url, albums_name, durations


import time

def qdrant_recommend(sp, collection_name, features, payload, limit=50):

    client = QdrantClient("localhost", port=6333, timeout=10)

    info = client.get_collection(collection_name=collection_name)

    size = info.vectors_count

    vectors = features.tolist()

    vectors_to_push = []
    payloads_to_push = []
    ids = []
    for i in range(len(payload)):
        track_name = payload[i]["track_name"]
        artist_name = payload[i]["artist_name"]
        search = client.scroll(
            collection_name=collection_name,
            scroll_filter=models.Filter(
            must=[
                models.FieldCondition(key="track_name", match=models.MatchValue(value=track_name)),
                models.FieldCondition(key="artist_name", match=models.MatchValue(value=artist_name)),
            ]
            ),
            limit=1,
            with_payload=True,
            with_vectors=False,
            )   
        is_present = len(search[0]) != 0
        if is_present:
            ids.append(search[0][0].id)
        else:
            vectors_to_push.append(vectors[i])
            payloads_to_push.append(payload[i])

    
    new_ids = list(range(size, size + len(vectors_to_push)))
    if len(new_ids) > 0:
        client.upsert(
            collection_name=collection_name,
            points=models.Batch(
                ids=new_ids,
                vectors=vectors_to_push,
                payloads=payloads_to_push
            )
        )


    ids.extend(new_ids)

    recommendation_list = client.recommend(
        collection_name=collection_name,
        positive=ids,
        limit=limit
    )

    results = []

    for result in recommendation_list:
        results.append(result.payload)

    track_ids = [pld["track_id"] for pld in results]

    images_url, albums_name, durations = get_album_images(sp, track_ids)


    for i, result in enumerate(results):
        result["image"] = images_url[i]
        result["album_name"] = albums_name[i]
        result["duration"] = durations[i]

    return results




def recommended(sp, limit=200, mode = "rp", track_name=None, artist_name=None, username=None):
    st = time.time()

    spotify_df = read_df()

    spotify_df = clean_df(spotify_df)

    # This depends on what the user selects 
    if mode == "rp":
        tracks, genres, payload = get_recently_played(sp)
        genre = get_main_genre(spotify_df, genres)
    elif mode == "tt":
        tracks, genres, payload = get_top_tracks(sp)
        genre = get_main_genre(spotify_df, genres)
    elif mode == "in":
        tracks, genre, payload = get_song_features(sp, spotify_df, track_name, artist_name, username)

    
    df_tracks = create_df_tracks(sp, tracks, genre)

    tracks_features = get_features(df_tracks)

    json_recommend = qdrant_recommend(sp, "spotify-vdb", tracks_features, payload, limit)


    # similarity_matrix = cosine_similarity(df_features, tracks_features)
    
    # similarity_vector = np.median(similarity_matrix, axis = 1)

    # recommended_idxs = np.argsort(similarity_vector)[::-1][1:limit + 1]

    # recommended_df = spotify_df[spotify_df.index.isin(recommended_idxs)].reindex(recommended_idxs)

    # print(recommended_df[["artist_name", "track_name", "track_id"]])#, "image_url"]])
    end = time.time()

    with open("./test.txt", "a") as f:
        f.write("time  = " + str(end-st) + "\n")

    return json_recommend#, "image_url"]].to_json()