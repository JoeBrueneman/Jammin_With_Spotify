from flask import Flask, request, render_template, render_template_string
import pickle
import numpy as np
from scipy.spatial import distance 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
import random
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import time
import urllib.parse as parse

# Load Spotify API key information into env variables
os.environ['SPOTIPY_CLIENT_ID']='eec42f936e1b4cfcab34e7980d9fe51e'  # "SPOTIPY" is not a typo
os.environ['SPOTIPY_CLIENT_SECRET']='2b4cb469bc554fedace8246bd14a7060'
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:3000'

# Create function which converts a playlist into its mean without touching the categorical variables
def playlist_mean(df):   
    df_avg=pd.DataFrame()
    df_avg.at[0,'danceability']=df['danceability'].mean()
    df_avg.at[0,'energy']=df['energy'].mean()
    df_avg.at[0,'loudness']=df['loudness'].mean()
    df_avg.at[0,'speechiness']=df['speechiness'].mean()
    df_avg.at[0,'acousticness']=df['acousticness'].mean()
    df_avg.at[0,'instrumentalness']=df['instrumentalness'].mean()
    df_avg.at[0,'liveness']=df['liveness'].mean()
    df_avg.at[0,'valence']=df['valence'].mean()
    df_avg.at[0,'tempo']=df['tempo'].mean()
    df_avg.at[0,'duration_ms']=df['duration_ms'].mean()
    df_avg.at[0,'key']=df['key'].mode().iloc[0]
    df_avg.at[0,'mode']=df['mode'].mode().iloc[0]
    df_avg.at[0,'time_signature']=df['time_signature'].mode().iloc[0]


    df_avg=df_avg.astype({"key":'int',"mode":'int',"time_signature":'int'})     # Does not remove the decimal ".0" even if it is an integer!
    df_avg['key']=df_avg['key'].astype(str)     # adding this line seems to convert "key", "mode", and "time_signature" to objects...


    df_avg=df_avg.assign(key_none=0,key_0=0,key_1=0,key_2=0,key_3=0,key_4=0,key_5=0,key_6=0,key_7=0,key_8=0,key_9=0,key_10=0,key_11=0,\
                mode_minor=0,mode_major=0,\
                time_signature_0=0,time_signature_1=0,time_signature_2=0,time_signature_3=0,time_signature_4=0,time_signature_5=0,time_signature_6=0,time_signature_7=0,)


    if df_avg.iloc[0]['key']==-1:
        df_avg.at[0,'key_none']=1
    else:
        col_name='key_'+str(df_avg.iloc[0]['key']) 
        df_avg.at[0,col_name]=1

    col_name='time_signature_'+str(df_avg.iloc[0]['time_signature']) 
    df_avg.at[0,col_name]=1

    if df_avg.iloc[0]['mode']==0:
        df_avg.at[0,'mode_minor']=1
    else:
        df_avg.at[0,'mode_major']=1   

    return df_avg

# Create function which converts a playlist into its weighted average via stddev without touching the categorical variables
def  playlist_mean_std(df):   
    df_avg=pd.DataFrame()
    df_avg.at[0,'danceability']=df['danceability'].mean()
    df_avg.at[0,'danceability_std']=df['danceability'].std()
    df_avg.at[0,'energy']=df['energy'].mean()
    df_avg.at[0,'energy_std']=df['energy'].std()
    df_avg.at[0,'loudness']=df['loudness'].mean()
    df_avg.at[0,'loudness_std']=df['loudness'].std()
    df_avg.at[0,'speechiness']=df['speechiness'].mean()
    df_avg.at[0,'speechiness_std']=df['speechiness'].std()
    df_avg.at[0,'acousticness']=df['acousticness'].mean()
    df_avg.at[0,'acousticness_std']=df['acousticness'].std()
    df_avg.at[0,'instrumentalness']=df['instrumentalness'].mean()
    df_avg.at[0,'instrumentalness_std']=df['instrumentalness'].std()
    df_avg.at[0,'liveness']=df['liveness'].mean()
    df_avg.at[0,'liveness_std']=df['liveness'].std()
    df_avg.at[0,'valence']=df['valence'].mean()
    df_avg.at[0,'valence_std']=df['valence'].std()
    df_avg.at[0,'tempo']=df['tempo'].mean()
    df_avg.at[0,'tempo_std']=df['tempo'].std()
    df_avg.at[0,'duration_ms']=df['duration_ms'].mean()
    df_avg.at[0,'duration_ms_std']=df['duration_ms'].std()
    df_avg.at[0,'key']=df['key'].mode().iloc[0]
    df_avg.at[0,'mode']=df['mode'].mode().iloc[0]
    df_avg.at[0,'time_signature']=df['time_signature'].mode().iloc[0]


    df_avg=df_avg.astype({"key":'int',"mode":'int',"time_signature":'int'})     # Does not remove the decimal ".0" even if it is an integer!
    df_avg['key']=df_avg['key'].astype(str)     # adding this line seems to convert "key", "mode", and "time_signature" to objects...


    df_avg=df_avg.assign(key_none=0,key_0=0,key_1=0,key_2=0,key_3=0,key_4=0,key_5=0,key_6=0,key_7=0,key_8=0,key_9=0,key_10=0,key_11=0,\
                mode_minor=0,mode_major=0,\
                     time_signature_0=0,time_signature_1=0,time_signature_2=0,time_signature_3=0,time_signature_4=0,time_signature_5=0,time_signature_6=0,time_signature_7=0)



    if df_avg.iloc[0]['key']==-1:
        df_avg.at[0,'key_none']=1
    else:
        col_name='key_'+str(df_avg.iloc[0]['key']) 
        # df_avg.at[0,col_name]=df_avg.iloc[0]['key']
        df_avg.at[0,col_name]=1

    col_name='time_signature_'+str(df_avg.iloc[0]['time_signature']) 
    # df_avg.at[0,col_name]=df_avg.iloc[0]['time_signature']
    df_avg.at[0,col_name]=1

    if df_avg.iloc[0]['mode']==0:
        df_avg.at[0,'mode_minor']=1
    else:
        df_avg.at[0,'mode_major']=1   

    return df_avg

# Function used to gather playlist information from Spotify
def gather_playlist_data(playlist_uri):
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    user_playist_track_uri = []
    for i in range (0,1000,100):
        playlist_info = spotify.playlist_items(playlist_uri, offset=i, limit=100)
        for x in range(0,len(playlist_info['items'])):
            user_playist_track_uri.append(playlist_info['items'][x]['track']['uri'])
        if len(playlist_info['items']) < 100:
            break
    
    return user_playist_track_uri
    
# Function used to create dummy variables for input to ML model from base track feature data
def dummy_variables(data):
    key_to_add = ['key_none', 'key_0', 'key_1', 'key_2',
    'key_3', 'key_4', 'key_5', 'key_6', 'key_7', 'key_8', 'key_9', 'key_10',
    'key_11']
    mode_to_add = ['mode_minor', 'mode_major']
    signature_to_add = ['time_signature_0', 'time_signature_1', 'time_signature_2', 'time_signature_3', 
                        'time_signature_4', 'time_signature_5', 'time_signature_6', 'time_signature_7']
    y = -1
    for x in key_to_add:
        for i in data:
            if i['key'] == y:
                i[x] = 1
            else:
                i[x] = 0
        y+=1
    for i in data:
        if i['mode'] == 1:
            i[mode_to_add[0]] = 0
            i[mode_to_add[1]] = 1
        else:
            i[mode_to_add[0]] = 1
            i[mode_to_add[1]] = 0
    time_signature = 0
    for x in signature_to_add:
        for i in data:
            if i['time_signature'] == time_signature:
                i[x] = 1
            else:
                i[x] = 0
        time_signature +=1

# Function used to gather track feature data
def gather_track_features(uri_track_list):
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    b = len(uri_track_list)
    results_full = []
    for i in range(0,b,100):
        if (b - i) < 100:
            x=uri_track_list[i:i+(b-i)]
            y=spotify.audio_features(x)
            results_full = results_full + y
        else:
            x=uri_track_list[i:i+100]
            y=spotify.audio_features(x)
            results_full = results_full + y
        time.sleep(0.5)
    
    return results_full

# Read the playlist_ID_trackURI csv file into a pandas DataFrame
playlist_ID_trackuri = pd.read_csv("./Resources/playlist_ID_trackuri.csv")

# Read the Playlist clustering csv file into a pandas DataFrame
playlist_weight_df = pd.read_csv("./Resources/scaled_playlist_clusters17.csv")

# Load model to test
model_pkl_file = "./Resources/playlist_std_mode_cluster17_model.pkl" 
with open(model_pkl_file, 'rb') as file:  
    model = pickle.load(file)

# Import the scaler used during creation of the playlist ML model
scaler = pickle.load(open('./Resources/scaler_playlist_std_mode_cluster17.sav', 'rb'))

# Import scaler from track vectors, as this data is different from playlist data above
scaler_vectors = pickle.load(open('./Resources/scaler_track_vectors.sav', 'rb'))

# Create Flask routes
app = Flask(__name__)

@app.route('/')
def home():
    results={}
    return render_template('index.html')

@app.route('/model_recommendation', methods=['POST','GET'])
def model_recommendation():
    if request.method == 'POST':
        # Extract input features from the request
        playlist_uri = str(request.form['track1'])

        # Parse out playlist uri from playlist link
        res = parse.urlparse(playlist_uri)
        res.path[10:-1]

        # Establish a connection with the Spotify API
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

        # Gather all track URI's from the user's playlist
        user_playist_track_uri = gather_playlist_data(playlist_uri)

        # Request track data from spotify on the 5 track slice from the user playlist
        data = gather_track_features(user_playist_track_uri)

        # Create dummy variable cells for later input into the model
        dummy_variables(data)

        # Create dataframe from data and create a copy for later use
        user_playlist_data_df = pd.DataFrame(data, columns=['danceability','energy', 'loudness', 'speechiness',
                    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                    'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms','key','mode','time_signature', 
                    'mode_minor', 'mode_major','key_none', 'key_0', 'key_1', 
                    'key_2', 'key_3', 'key_4', 'key_5', 'key_6', 'key_7', 'key_8', 
                    'key_9', 'key_10', 'key_11', 'time_signature_0', 'time_signature_1',
                    'time_signature_2', 'time_signature_3', 'time_signature_4', 'time_signature_5',
                    'time_signature_6', 'time_signature_7'])
        user_playlist_model_data_df = user_playlist_data_df.copy()

        # Create the weighted data from the users_playlist
        user_playlist_weighted_df = playlist_mean_std(user_playlist_model_data_df)

        # Drop columns not needed for modeling
        user_playlist_weighted_df = user_playlist_weighted_df.drop(['key', 'mode', 'time_signature'], axis=1)

        # Scale input_playlist
        scaled_user_playlist_data = scaler.transform(user_playlist_weighted_df)
        scaled_user_playlist_weighted_df = pd.DataFrame(scaled_user_playlist_data,columns=user_playlist_weighted_df.columns, 
                                                        index=user_playlist_weighted_df.index)

        # Make cluster prediction using the loaded model
        prediction = model.predict(scaled_user_playlist_weighted_df)

        # Isolate playlists within predicted cluster
        recommend_playlists = playlist_weight_df[playlist_weight_df["playlist_clusters"]==prediction[0]]

        # Use cosine similarity to find the 5 closest playlists to the user's playlist within the model
        recommend_playlists_df = recommend_playlists.drop(['playlist_clusters'],axis=1)
        recommend_playlists_df=recommend_playlists_df.set_index('pid')
        recommend_playlists_df['similarity'] = cosine_similarity(recommend_playlists_df.values, scaled_user_playlist_weighted_df.values)
        recommend_playlists_df_top_5 = recommend_playlists_df.sort_values('similarity', ascending=False).head(5)

        # Reset index to return the PID data to a column
        recommend_playlists_df_top_5 = recommend_playlists_df_top_5.reset_index()

        # Gather track uri's from the 5 closest playlists, drop all other columns and remove duplicates
        recommended_df = pd.merge(recommend_playlists_df_top_5, playlist_ID_trackuri, on='pid')
        recommended_df = recommended_df[['pid','track_uri']]
        recommended_df = recommended_df.drop_duplicates(subset=['track_uri'])
        recommended_track_uri_df = recommended_df[['track_uri']]

        # Compare tracks in the 3 closest playlists to the users playlist to remove those already included
        recommended_track_uri_df = recommended_track_uri_df[~recommended_track_uri_df['track_uri'].isin(user_playist_track_uri)]
        recommended_track_list = list(recommended_track_uri_df['track_uri'])

        # If list empty, return message
        if len(recommended_track_list) == 0:
             return render_template('index.html', "The recommended playlist's contain no songs that were not already in the user's playlist")
        
        # Gather track data from API for the recommended tracks
        recommended_track_data = gather_track_features(recommended_track_list)

        # Create copy of original user input dataset, to take the mean instead of the weight
        user_playlist_mean_data_df = user_playlist_data_df.copy()
        user_playlist_mean_data_df = playlist_mean(user_playlist_mean_data_df)

        # Create dummy variable cells for later input into the model
        dummy_variables(recommended_track_data)
        
        # Format dataframes for input to model
        recommendation_track_data_df = pd.DataFrame(recommended_track_data, columns=['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                    'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms',
                    'time_signature', 'key_none', 'key_0', 'key_1', 
                    'key_2', 'key_3', 'key_4', 'key_5', 'key_6', 'key_7', 'key_8', 
                    'key_9', 'key_10', 'key_11', 'mode_minor', 'mode_major','time_signature_0', 'time_signature_1',
                    'time_signature_2', 'time_signature_3', 'time_signature_4', 'time_signature_5',
                    'time_signature_6', 'time_signature_7'])
        recommendation_track_data_df=recommendation_track_data_df.set_index('uri')
        recommendation_track_data_df = recommendation_track_data_df.drop(['key','type', 'id', 'track_href', 'analysis_url','mode','time_signature'], axis=1)
        user_playlist_mean_data_df = user_playlist_mean_data_df.drop(['key', 'mode', 'time_signature'], axis=1)

        # Scale recommendation_track_data_df
        scaled_recommended_df = scaler_vectors.transform(recommendation_track_data_df)
        recommendation_track_data_df = pd.DataFrame(scaled_recommended_df,columns=recommendation_track_data_df.columns, 
                                                    index=recommendation_track_data_df.index)
        
        # Scale user_playlist_mean_data_df
        scaled_user_df = scaler_vectors.transform(user_playlist_mean_data_df)
        user_playlist_mean_data_df = pd.DataFrame(scaled_user_df,columns=user_playlist_mean_data_df.columns, 
                                                    index=user_playlist_mean_data_df.index)
        
        # Use cosine similarity to find the closest tracks to the input mean playlist
        recommendation_track_data_df['similarity'] = cosine_similarity(recommendation_track_data_df.values, user_playlist_mean_data_df.values)
        recommend_tracks_df_top_5 = recommendation_track_data_df.sort_values('similarity', ascending=False)
        recommend_tracks_df_top_5.head()

        # Reset index to return the track URI data to a column
        recommend_tracks_df_top_5 = recommend_tracks_df_top_5.reset_index()

        # Gather 5 track URI's from the recommended dataframe
        recommended_track_uri_list = []
        for x in range(0,5,1):
            recommended_track_uri_list.append(recommend_tracks_df_top_5['uri'][x])

        # Gather information from spotify on the 5 songs to recommend
        tracks_info = spotify.tracks(recommended_track_uri_list)

        # Compile recommended track data
        results = []
        for x in range(0,len(recommended_track_uri_list)):
            result_dict = {}
            result_dict['Track URI'] = tracks_info['tracks'][x]['uri']
            result_dict['Album Cover'] = tracks_info['tracks'][x]['album']['images'][0]['url']
            result_dict['Track Name'] = tracks_info['tracks'][x]['name']
            result_dict['Artist Name'] = tracks_info['tracks'][x]['artists'][0]['name']
            result_dict['Preview URL'] = tracks_info['tracks'][x]['preview_url']
            results.append(result_dict)

        return render_template('result.html', result1=results[0], result2=results[1], result3=results[2], result4=results[3], result5=results[4])

# Run the Flask App locally
if __name__ == '__main__':
    app.run(debug=True)