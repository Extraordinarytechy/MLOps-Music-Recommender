import joblib
from melorec.config import MODEL_PATH, DATABASE_URI
from sqlalchemy import create_engine, text
import pandas as pd
from typing import List

# --- Database and Model Loading ---
try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully.")
except FileNotFoundError:
    print(f"Error: Model file not found at {MODEL_PATH}")
    model = None

try:
    engine = create_engine(DATABASE_URI)
    print("Database connection established.")
except Exception as e:
    print(f"Error connecting to database: {e}")
    engine = None

# Get all song IDs for prediction
def get_all_song_ids():
    if engine is None:
        return []
    
    with engine.connect() as conn:
        query = text("SELECT song_id FROM songs")
        result = conn.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df['song_id'].unique().tolist()

ALL_SONG_IDS = get_all_song_ids()
print(f"Loaded {len(ALL_SONG_IDS)} song IDs for prediction.")


def get_song_details(song_ids: List[str]) -> pd.DataFrame:
    """
    Fetches the title and artist for a list of song IDs from the database.
    """
    if engine is None:
        return pd.DataFrame(columns=['song_id', 'title', 'artist'])
        
    with engine.connect() as conn:
        # We use :ids to safely pass our list of IDs
        query = text("""
            SELECT song_id, title, artist 
            FROM songs 
            WHERE song_id = ANY(:ids)
        """)
        
        result = conn.execute(query, {'ids': song_ids})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df


# ---  PREDICTION FUNCTION ---
def generate_recommendations(user_id: str, n: int = 10) -> List[dict]:
    if model is None:
        raise RuntimeError("Model is not loaded.")
    if engine is None:
        raise RuntimeError("Database is not connected.")
    
    print(f"Generating recommendations for user: {user_id}")
    
    # 1. Predict scores for all songs for this user
    predictions = []
    for song_id in ALL_SONG_IDS:
        pred = model.predict(uid=user_id, iid=song_id)
        predictions.append({
            "song_id": song_id,
            "estimated_score": pred.est
        })
    
    # 2. Sort by score
    predictions.sort(key=lambda x: x["estimated_score"], reverse=True)
    
    # 3. Get Top N
    top_n_preds = predictions[:n]
    top_n_song_ids = [pred['song_id'] for pred in top_n_preds]

    # 4. --- Get song details ---
    details_df = get_song_details(top_n_song_ids)
    
    # 5. --- Join details with scores ---
    final_recommendations = []
    for pred in top_n_preds:
        song_details = details_df[details_df['song_id'] == pred['song_id']].to_dict('records')
        
        if song_details:
            final_rec = {
                "song_id": pred['song_id'],
                "title": song_details[0]['title'],
                "artist": song_details[0]['artist'],
                "estimated_score": pred['estimated_score']
            }
            final_recommendations.append(final_rec)
            
    return final_recommendations