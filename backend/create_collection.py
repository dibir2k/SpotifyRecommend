import pandas as pd
import time
import os
from qdrant_client import QdrantClient, models

DIR = "./app/csvFiles"

def read_df():
    df = pd.read_csv(DIR + "/spotify_data.csv")
    df.drop(df.columns[0], axis=1, inplace=True)
    df = df.fillna("None", inplace=False)

    return df

def get_all_features(df):
    total_df = pd.get_dummies(df, columns=["genre"], dtype="int64")
    for col in total_df.columns:
        if total_df[col].dtype == "float64":
            total_df[col] = (total_df[col] - total_df[col].mean()) / total_df[col].std()
    return total_df.to_numpy()

def to_features(df):
     # Drop unnecessary columns
    features_df = df.drop(["artist_name", "year", "track_id", "track_name", "duration_ms", "key", "time_signature", "popularity"], axis=1)
    return features_df

def upsert_with_retries(client, collection_name, ids, vectors, payloads, max_retries=5):
    for attempt in range(max_retries):
        try:
            client.upsert(
                collection_name=collection_name,
                points=models.Batch(
                    ids=ids,
                    vectors=vectors,
                    payloads=payloads
                )
            )
            return
        except:
            time.sleep(2 ** attempt)  # Exponential backoff
    raise RuntimeError(f"Failed to upsert data after {max_retries} attempts")

def init_collection(collection_name, data, sp_df):
    dims = data.shape[1]
    client = QdrantClient('qdrant', port=6333, timeout=30)

    # Create collection if it doesn't exist
    try:
        client.get_collection(collection_name=collection_name)
    except:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=dims, distance=models.Distance.COSINE),
            optimizers_config=models.OptimizersConfigDiff(memmap_threshold=20000, indexing_threshold=0),
            quantization_config=models.ScalarQuantization(
                scalar=models.ScalarQuantizationConfig(
                    type=models.ScalarType.INT8,
                    always_ram=True,
                ),
            ),
        )

    payload = sp_df[["artist_name", "track_name", "track_id"]].to_dict('records')
    vectors = data.tolist()
    size = len(vectors)

    batch_size = 20000
    index = list(range(size))

    for i in range(0, size, batch_size):
        ids = index[i:i+batch_size]
        print(f"Upserting batch {i // batch_size + 1}/{(size // batch_size) + 1}")
        upsert_with_retries(client, collection_name, ids, vectors[i:i+batch_size], payload[i:i+batch_size])


if __name__ == "__main__":
    is_collection =  os.path.isdir("./qdrant_storage") and len(os.listdir("./qdrant_storage/collections")) != 0
    if not is_collection:
        spotify_df = read_df()
        features_df = to_features(spotify_df)
        data = get_all_features(features_df)

        init_collection("spotify-vdb", data, spotify_df)