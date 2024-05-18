import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Spotify API credentials
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8888/callback'

# Check if environment variables are set
if not CLIENT_ID or not CLIENT_SECRET:
    logging.error("Spotify API credentials are not set in the environment variables.")
    raise EnvironmentError("Spotify API credentials are missing.")

# Authentication
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri=REDIRECT_URI,
                                                   scope="user-read-recently-played"))
    logging.info("Spotify authentication successful.")
except spotipy.exceptions.SpotifyOauthError as e:
    logging.error(f"Spotify OAuth error: {e}")
    raise
except Exception as e:
    logging.error(f"Unexpected error during authentication: {e}")
    raise

def get_recently_played():
    try:
        # Fetch recently played tracks
        results = sp.current_user_recently_played(limit=50)
        tracks = results['items']

        # Extracting data
        data = []
        for track in tracks:
            track_info = track['track']
            played_at = track['played_at']
            data.append({
                'Track Name': track_info['name'],
                'Artist': track_info['artists'][0]['name'],
                'Played At': played_at
            })

        logging.info(f"Fetched {len(data)} tracks.")
        return data
    except spotipy.exceptions.SpotifyException as e:
        logging.error(f"Error fetching recently played tracks: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return []

def save_to_excel(data, filename="spotify_listening_history.xlsx"):
    try:
        # Load existing data or create a new dataframe
        if os.path.exists(filename):
            df_existing = pd.read_excel(filename)
        else:
            df_existing = pd.DataFrame(columns=['Track Name', 'Artist', 'Played At'])

        # Append new data to the dataframe
        df_new = pd.DataFrame(data)
        df_combined = pd.concat([df_existing, df_new]).drop_duplicates().reset_index(drop=True)

        # Save to Excel file
        df_combined.to_excel(filename, index=False)
        logging.info(f"Data saved to {filename}.")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except pd.errors.ParserError as e:
        logging.error(f"Error processing Excel file: {e}")
    except ImportError as e:
        logging.error(f"Import error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Fetch and save data
    data = get_recently_played()
    if data:
        save_to_excel(data)
    else:
        logging.warning("No data fetched, nothing to save.")

# AWS Lambda function to collect Spotify data
import json

def lambda_handler(event, context):
    try:
        data = get_recently_played()
        if data:
            save_to_excel(data)
            response_message = "Data collection successful!"
        else:
            response_message = "No data fetched, nothing to save."
    except Exception as e:
        logging.error(f"Error in lambda_handler: {e}")
        response_message = f"Error: {e}"

    return {
        'statusCode': 200,
        'body': json.dumps(response_message)
    }
