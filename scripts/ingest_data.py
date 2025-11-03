import pandas as pd
from sqlalchemy import create_engine, text
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from melorec.config import DATABASE_URI
except ImportError:
    print("Error: Could not import DATABASE_URI.")
    print("Make sure you are running this script from the root 'MeloRec' folder.")
    DATABASE_URI = "postgresql://admin:secret@localhost:5433/melorec_db" # Make sure this port is 5433


def ingest_data():
    try:
        engine = create_engine(DATABASE_URI)
        print("Connecting to database...")
        
        print("Creating schema (tables)...")
        with engine.connect() as conn:
            with open('scripts/setup_database.sql', 'r') as f:
                sql_script = f.read()
                conn.execute(text(sql_script))
            conn.commit()
        print("Schema created.")

        # --- Ingest users.csv ---
        print("Ingesting users...")
        df_users = pd.read_csv('data/users.csv')
        # Add drop_duplicates just in case
        df_users.drop_duplicates(subset=['user_id'], inplace=True) 
        df_users.to_sql('users', engine, if_exists='append', index=False)
        print(f"Ingested {len(df_users)} users.")
        
        # --- Ingest songs.csv ---
        print("Ingesting songs...")
        df_songs = pd.read_csv('data/songs.csv')
        df_songs.rename(columns={'artist_name': 'artist'}, inplace=True)
        
        # Remove any duplicate song_ids from the CSV file before inserting
        df_songs.drop_duplicates(subset=['song_id'], inplace=True)
        # ----------------------
        
        df_songs.to_sql('songs', engine, if_exists='append', index=False)
        print(f"Ingested {len(df_songs)} songs.")

        # --- Ingest play_history.csv ---
        print("Ingesting play history...")
        df_history = pd.read_csv('data/play_history.csv')
        df_history.to_sql('play_history', engine, if_exists='append', index=False)
        print(f"Ingested {len(df_history)} play history records.")
        
        print("\nData ingestion complete!")

    except Exception as e:
        print(f"\n--- AN ERROR OCCURRED ---")
        print(f"Error: {e}")
        print("Common fixes:")
        print("1. Is your Docker container running? (Run 'docker compose up -d')")
        print("2. Are the files 'users.csv', 'songs.csv', 'play_history.csv' in the 'data/' folder?")
        print("3. Did you already run this script? (Data might already be in the DB)")
        sys.exit(1)

if __name__ == "__main__":
    ingest_data()