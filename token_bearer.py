
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set your Spotify API credentials

client_id = ""
client_secret = ""
redirect_uri = 'https://accounts.spotify.com/authorize'
# Initialize the Spotify client with authentication
sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='user-library-read')

# Get the authorization URL
auth_url = sp_oauth.get_authorize_url()

# Open the authorization URL in a web browser
import webbrowser
webbrowser.open(auth_url)

# After authorizing your app, Spotify will redirect to the specified redirect_uri with the authorization code.
# Extract the authorization code from the URL. You can manually copy it from the address bar.
# For example, if the URL is http://localhost:8080/callback?code=YOUR_CODE, extract YOUR_CODE.

# Set the authorization code here
authorization_code = 'YOUR_CODE'

# Request the Bearer Token using the authorization code
token_info = sp_oauth.get_access_token(authorization_code)

# The Bearer Token is now stored in the token_info dictionary
bearer_token = token_info['access_token']

print(f'Spotify Bearer Token: {bearer_token}')
