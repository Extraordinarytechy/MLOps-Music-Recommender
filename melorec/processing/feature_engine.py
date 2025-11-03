import pandas as pd
from sqlalchemy import create_engine
from melorec.config import DATABASE_URI

def get_training_data():
    
    query = """
    WITH user_song_plays AS (
        -- Aggregate total plays per user per song
        SELECT 
            user_id, 
            song_id, 
            SUM(play_count) as total_plays
        FROM play_history
        GROUP BY user_id, song_id
    ),
    user_play_stats AS (
        -- Get stats per user to calculate a 'rating'
        SELECT
            user_id,
            MAX(total_plays) as max_plays,
            MIN(total_plays) as min_plays
        FROM user_song_plays
        GROUP BY user_id
    )
    -- Create a normalized 1-5 star rating
    SELECT 
        usp.user_id,
        usp.song_id,
        -- Scale plays to a 1-5 rating. Add 1 to avoid 0/0.
        CASE 
            WHEN (ups.max_plays - ups.min_plays) = 0 THEN 1
            ELSE 
                1 + (4 * (usp.total_plays - ups.min_plays) / NULLIF((ups.max_plays - ups.min_plays), 0))
        END as rating
    FROM user_song_plays usp
    JOIN user_play_stats ups ON usp.user_id = ups.user_id;
    """
    
    engine = create_engine(DATABASE_URI)
    df = pd.read_sql(query, engine)
    return df