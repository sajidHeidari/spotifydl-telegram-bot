import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
import logging

logger = logging.getLogger(__name__)

def get_playlist_tracks(playlist_link: str, client_id: str, client_secret: str) -> list | None:
    """Fetches all track names from a Spotify playlist link."""
    try:
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(auth_manager=auth_manager)

        playlist_id = playlist_link.split("/")[-1].split("?")[0]
        results = sp.playlist_tracks(playlist_id)
        
        tracks = []
        while results:
            for item in results['items']:
                track = item.get('track')
                if track and track.get('artists'):
                    track_name = f"{track['artists'][0]['name']} - {track['name']}"
                    tracks.append(track_name)
            
            if results['next']:
                results = sp.next(results)
            else:
                results = None
        
        logger.info(f"Fetched {len(tracks)} tracks from playlist {playlist_id}.")
        return tracks

    except Exception as e:
        logger.error(f"Could not fetch playlist '{playlist_link}'. Error: {e}")
        return None


def download_audio(track_name: str, download_path: str = "downloads") -> str | None:
    """Searches a track on YouTube, downloads it as an MP3, and returns the file path."""
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_query = f"ytsearch1:{track_name}"
            info = ydl.extract_info(search_query, download=True)['entries'][0]
            
            filename_base = ydl.prepare_filename(info)
            mp3_filepath = os.path.splitext(filename_base)[0] + '.mp3'

            if os.path.exists(mp3_filepath):
                logger.info(f"Successfully downloaded: {mp3_filepath}")
                return mp3_filepath
            return None

    except Exception as e:
        logger.error(f"Failed to download '{track_name}'. Error: {e}")
        return None
