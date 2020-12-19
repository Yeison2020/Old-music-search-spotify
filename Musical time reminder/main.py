from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Scraping Billboard 100

date = input("Which year do you want to travel to ? type the date in this format YYYY-MM-DD\n")
try:

    URL_100_SONGS="https://www.billboard.com/charts/hot-100/" + date
except:
    print("Date is not available")

else:

    response = requests.get(URL_100_SONGS)
    Data_songs = response.text
    soup = BeautifulSoup(Data_songs, "html.parser")
    SONGS_BEST = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
    SONGS_NAME = [ song.getText() for song in SONGS_BEST]
    print(SONGS_NAME)


#Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=YOUR CLIENT ID,
        client_secret=YOUR CLIENT SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

song_uris = []
year = date.split("-")[0]
for song in SONGS_NAME:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

#Adding songs found into the new playlist
sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist["id"], tracks=song_uris)