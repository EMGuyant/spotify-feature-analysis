import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

#Update with appropriate client ID and client secret explicitly or by other methods
client_credentials_manager = SpotifyClientCredentials(
    client_id='CLIENT_ID', 
    client_secret='CLIENT_SECRET')

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#List of data stored for each track
feature_list = ['track_id', 'track_name', 'artist', 'album_type', 'release_date', 'decade', 'popularity',
    'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
    'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

#Define data frames for each decade of interest
df_tracks60s = pd.DataFrame(columns = feature_list)
df_tracks70s = pd.DataFrame(columns = feature_list)
df_tracks80s = pd.DataFrame(columns = feature_list)
df_tracks90s = pd.DataFrame(columns = feature_list)
df_tracks00s = pd.DataFrame(columns = feature_list)
df_tracks10s = pd.DataFrame(columns = feature_list)
df_tracks = pd.DataFrame(columns = feature_list)

#List of decade yearly ranges to pass to sp.search
years_list = ['1960-1969', '1970-1979', '1980-1989', '1990-1999', '2000-2009', '2010-2019']

for year in years_list:
    print(year)
    #Maximum returned results per request is 50 for loop makes 20 requests
    for i in range(20):
        #Spotify API Search call 
        results=sp.search(q='genre:country year:' + year + '', market='US', type='track', limit=50, offset=i*50)['tracks']
       
        #Loop through tracks and extract/append features
        for track in results['items']:
            track_features = {}
            
            #Extract metadata
            track_features['track_id'] = track['id']
            track_features['track_name'] = track['name']
            track_features['artist'] = track['artists'][0]['name']
            track_features['album_type'] = track['album']['album_type']
            track_features['release_date'] = track['album']['release_date']
            track_features['decade'] = track_features['release_date'][:3] + '0'
            track_features['popularity'] = track['popularity']

            #Extract track audio features
            audio_features = sp.audio_features(track['id'])[0]
            #For each feature in the above defined list starting with danceability
            #(index 5)
            for feature in feature_list[7:]:
                track_features[feature] = audio_features[feature]

            #Concatentate the dataframes
            df_track_features = pd.DataFrame(track_features, index=[0])
            #All tracks dataframe
            df_tracks = pd.concat([df_tracks, df_track_features], ignore_index=True)

            #Decade specific dataframes
            if year.find('60') != -1:
                df_tracks60s = pd.concat([df_tracks60s, df_track_features], ignore_index = False)
                df_tracks60s.to_csv('./data/tracks60s.csv')
            elif year.find('70') != -1:
                df_tracks70s = pd.concat([df_tracks70s, df_track_features], ignore_index = True)
                df_tracks70s.to_csv('./data/tracks70s.csv')
            elif year.find('80') != -1:
                df_tracks80s = pd.concat([df_tracks80s, df_track_features], ignore_index = True)
                df_tracks80s.to_csv('./data/tracks80s.csv')
            elif year.find('90') != -1:
                df_tracks90s = pd.concat([df_tracks90s, df_track_features], ignore_index = True)
                df_tracks90s.to_csv('./data/tracks90s.csv')
            elif year.find('00') != -1:
                df_tracks00s = pd.concat([df_tracks00s, df_track_features], ignore_index = True)
                df_tracks00s.to_csv('./data/tracks00s.csv')
            else:
                df_tracks10s = pd.concat([df_tracks10s, df_track_features], ignore_index = True)
                df_tracks10s.to_csv('./data/tracks10s.csv')

df_tracks.to_csv('tracks.csv')