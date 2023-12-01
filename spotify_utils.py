from typing import List
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from chat_utils import Playlist, Song


class SpotifyClient:
    def __init__(self):
        # Set up authentication
        scope = 'playlist-modify-public playlist-read-private user-library-read'
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, open_browser=False))
    
    def get_user_songs(self) -> List[Song]:

        # Get the current user's liked songs and add them to the all_user_songs list
        all_user_songs: List[Song] = []
        results = self.sp.current_user_saved_tracks()
        all_user_songs.extend(self._get_all_tracks(results))

        # Get the current user's playlists
        playlists = self.sp.current_user_playlists(limit=50)  # Max limit
        user_id = self.sp.me()['id']

        # Iterate through each playlist and add the songs to the all_user_songs list
        for playlist in playlists['items']:
            if playlist['owner']['id'] == user_id:
                results = self.sp.playlist_tracks(playlist['id'])
                all_user_songs.extend(self._get_all_tracks(results))

        return all_user_songs

    def add_playlist(self, playlist: Playlist):
        # Create a playlist
        new_playlist = self.sp.user_playlist_create(user=self.sp.current_user()['id'], name=playlist.title)

        track_ids = [] 
        for song in playlist.songs:
            # Search tracks
            # result = self.sp.search(f"{song.artist} {song.title}", type='track', limit=1) # Non-exact search
            result = self.sp.search(f"artist:{song.artist} track:{song.title}", type='track', limit=1) # Non-exact search
            
            # Assuming you want the first search result
            if result['tracks']['items']:
                # Get the Spotify track ID
                track_id = result['tracks']['items'][0]['id']
                track_ids.append(f"spotify:track:{track_id}")
                print(f"Song found: {song.title} by {song.artist}")
            else:
                print(f"No results for {song.title} by {song.artist}")

        # Add tracks
        self.sp.playlist_add_items(playlist_id=new_playlist['id'], items=track_ids)

    def _get_all_tracks(self, tracks):
        """Function to handle pagination and extract songs"""
        songs = []
        while tracks:
            songs.extend([Song(title=item['track']['name'], artist=item['track']['artists'][0]['name']) for item in tracks['items']])
            if tracks['next']:
                tracks = self.sp.next(tracks)
            else:
                break
        return songs