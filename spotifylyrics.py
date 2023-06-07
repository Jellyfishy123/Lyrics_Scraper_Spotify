import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
import requests

#https://developer.spotify.com/dashboard/662bd8bc9ced464eb7f256b272662385/settings

cid ='662bd8bc9ced464eb7f256b272662385'
secret ='b106dda4cc9046d9bd7a35cdd798ee7b'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#insert the URI as a string into the function
def get_album_tracks(uri_info):
    uri = []
    track = []
    duration = []
    explicit = []
    track_number = []
    one = sp.album_tracks(uri_info, limit=50, offset=0, market='US')
    df1 = pd.DataFrame(one)
    
    for i, x in df1['items'].items():
        uri.append(x['uri'])
        track.append(x['name'])
        duration.append(x['duration_ms'])
        explicit.append(x['explicit'])
        track_number.append(x['track_number'])
    
    df2 = pd.DataFrame({
    'uri':uri,
    'track':track,
    'duration_ms':duration,
    'explicit':explicit,
    'track_number':track_number})
    
    return df2

#print(get_album_tracks('https://open.spotify.com/album/1pCA38N6MkLlthXtAOvZTU?si=8Ud6PA2cSHiDqmyp7Zod9g'))

#insert output dataframe from the get_album_tracks function
def get_track_info(df):
    danceability = []
    energy = []
    key = []
    loudness = []
    speechiness = []
    acousticness = []
    instrumentalness = []
    liveness = []
    valence = []
    tempo = []
    for i in df['uri']:
        for x in sp.audio_features(tracks=[i]):
            danceability.append(x['danceability'])
            energy.append(x['energy'])
            key.append(x['key'])
            loudness.append(x['loudness'])
            speechiness.append(x['speechiness'])
            acousticness.append(x['acousticness'])
            instrumentalness.append(x['instrumentalness'])
            liveness.append(x['liveness'])
            valence.append(x['valence'])
            tempo.append(x['tempo'])
            
    df2 = pd.DataFrame({
    'danceability':danceability,
    'energy':energy,
    'key':key,
    'loudness':loudness,
    'speechiness':speechiness,
    'acousticness':acousticness,
    'instrumentalness':instrumentalness,
    'liveness':liveness,
    'valence':valence,
    'tempo':tempo})
    
    return df2

#print(get_track_info(get_album_tracks('https://open.spotify.com/album/1pCA38N6MkLlthXtAOvZTU?si=8Ud6PA2cSHiDqmyp7Zod9g')))

df1 = get_album_tracks('https://open.spotify.com/album/1pCA38N6MkLlthXtAOvZTU?si=8Ud6PA2cSHiDqmyp7Zod9g')

df2 = get_track_info(get_album_tracks('https://open.spotify.com/album/1pCA38N6MkLlthXtAOvZTU?si=8Ud6PA2cSHiDqmyp7Zod9g'))

def merge_frames(df1, df2):
    df3 = df1.merge(df2, left_index= True, right_index= True)
    return df3

#print(merge_frames(df1, df2))

#function to scrape lyrics from genius
def scrape_lyrics(artistname, songname):
    artistname2 = str(artistname.replace(' ','-')) if ' ' in artistname else str(artistname)
    songname2 = str(songname.replace(' ','-')) if ' ' in songname else str(songname)
    page = requests.get('https://genius.com/'+ artistname2 + '-' + songname2 + '-' + 'lyrics')
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics1 = html.find("div", class_="lyrics")
    lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-2 jgQsqn")
    if lyrics1:
        lyrics = lyrics1.get_text()
    elif lyrics2:
        lyrics = lyrics2.get_text()
    elif lyrics1 == lyrics2 == None:
        lyrics = None
    return lyrics

#function to attach lyrics onto data frame
#artist_name should be inserted as a string
def lyrics_onto_frame(df1, artist_name):
    for i,x in enumerate(df1['track']):
        test = scrape_lyrics(artist_name, x)
        df1.loc[i, 'lyrics'] = test
    return df1


blonde_df1_tracks = get_album_tracks('spotify:album:3mH6qwIy9crq0I9YQbOuDf')
blonde_df2_metadata = get_track_info(blonde_df1_tracks)
df1 = merge_frames(blonde_df1_tracks, blonde_df2_metadata)
print(lyrics_onto_frame(df1, 'frank ocean'))
