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

scaler = StandardScaler()
os.environ['SPOTIPY_CLIENT_ID']='eec42f936e1b4cfcab34e7980d9fe51e'  # "SPOTIPY" is not a typo
os.environ['SPOTIPY_CLIENT_SECRET']='2b4cb469bc554fedace8246bd14a7060'
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:3000'

def playlist_weight(df):   
    df_wgt=pd.DataFrame()
    if df['danceability'].std()==0:
        x=0.0000001
    else:
        x=df['danceability'].std()
    df_wgt.at[0,'danceability']=df['danceability'].mean()/x

    if df['energy'].std()==0:
        x=0.0000001
    else:
        x=df['energy'].std()
    df_wgt.at[0,'energy']=df['energy'].mean()/x

    if df['loudness'].std()==0:
        x=0.0000001
    else:
        x=df['loudness'].std()
    df_wgt.at[0,'loudness']=df['loudness'].mean()/x

    if df['speechiness'].std()==0:
        x=0.0000001
    else:
        x=df['speechiness'].std()
    df_wgt.at[0,'speechiness']=df['speechiness'].mean()/x

    if df['acousticness'].std()==0:
        x=0.0000001
    else:
        x=df['acousticness'].std()
    df_wgt.at[0,'acousticness']=df['acousticness'].mean()/x

    if df['instrumentalness'].std()==0:
        x=0.00000013
    else:
        x=df['instrumentalness'].std()
    df_wgt.at[0,'instrumentalness']=df['instrumentalness'].mean()/x

    if df['liveness'].std()==0:
        x=0.0000001
    else:
        x=df['liveness'].std()
    df_wgt.at[0,'liveness']=df['liveness'].mean()/x

    if df['valence'].std()==0:
        x=0.0000001
    else:
        x=df['valence'].std()
    df_wgt.at[0,'valence']=df['valence'].mean()/x

    if df['tempo'].std()==0:
        x=0.0000001
    else:
        x=df['tempo'].std()
    df_wgt.at[0,'tempo']=df['tempo'].mean()/x

    if df['duration_ms'].std()==0:
        x=0.0000001
    else:
        x=df['duration_ms'].std()
    df_wgt.at[0,'duration_ms']=df['duration_ms'].mean()/x

    df_wgt.at[0,'key']=df['key'].mode().iloc[0]
    df_wgt.at[0,'mode']=df['mode'].mode().iloc[0]
    df_wgt.at[0,'time_signature']=df['time_signature'].mode().iloc[0]


    df_wgt=df_wgt.astype({"key":'int',"mode":'int',"time_signature":'int'})     # Does not remove the decimal ".0" even if it is an integer!
    df_wgt['key']=df_wgt['key'].astype(str)     # adding this line seems to convert "key", "mode", and "time_signature" to objects...


    df_wgt=df_wgt.assign(key_none=0,key_0=0,key_1=0,key_2=0,key_3=0,key_4=0,key_5=0,key_6=0,key_7=0,key_8=0,key_9=0,key_10=0,key_11=0,\
                mode_minor=0,mode_major=0,\
                time_signature_0=0,time_signature_1=0,time_signature_2=0,time_signature_3=0,time_signature_4=0,time_signature_5=0,time_signature_6=0,time_signature_7=0,)



    if df_wgt.iloc[0]['key']==-1:
        df_wgt.at[0,'key_none']=1
    else:
        col_name='key_'+str(df_wgt.iloc[0]['key']) 
        df_wgt.at[0,col_name]=df_wgt.iloc[0]['key']

    col_name='time_signature_'+str(df_wgt.iloc[0]['time_signature']) 
    df_wgt.at[0,col_name]=df_wgt.iloc[0]['time_signature']

    if df_wgt.iloc[0]['mode']==0:
        df_wgt.at[0,'mode_minor']=1
    else:
        df_wgt.at[0,'mode_major']=1   

    return df_wgt

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

# Read the csv file into a pandas DataFrame
playlist_weight_df = pd.read_csv("Resources/playlist_weightmode_cluster6.csv")

model_pkl_file = "Resources/Playlist_weightmode_cluster6.pkl" 
with open(model_pkl_file, 'rb') as file:  
    model = pickle.load(file)

# Read the playlist_ID_trackURI csv file into a pandas DataFrame
playlist_ID_trackuri = pd.read_csv("Resources/playlist_ID_trackuri.csv")

# Create Flask routes
app = Flask(__name__)

@app.route('/')
def home():
    results={}
    return render_template('index.html')

@app.route('/vector_model_prediction', methods=['POST','GET'])
def vector_model_prediction():
    if request.method == 'POST':
        # Extract input features from the request
        playlist_uri = str(request.form['track1'])

        model_pkl_file = "Resources/Playlist_weightmode_cluster6.pkl" 
        with open(model_pkl_file, 'rb') as file:  
            model = pickle.load(file)

        # Establish a connection with the Spotify API
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

        # Fit the data to the model
        scaler.fit(playlist_weight_df.drop('playlist_clusters',axis=1))

        # Gather all track URI's from the user's playlist
        user_playist_track_uri = gather_playlist_data(playlist_uri)

        # Create a slice of 5 random tracks from the users playlist
        random_selection = random.sample(range(1, len(user_playist_track_uri)), 20)
        sample_uri_list = []
        for x in random_selection:
            sample_uri_list.append(user_playist_track_uri[x])

        # Request track data from spotify on the 5 track slice from the user playlist
        data=spotify.audio_features(sample_uri_list)

        # Create dummy variable cells for later input into the model
        dummy_variables(data)



        # Create a datafram and edit column names and order to allow input to model
        user_playlist_data_df = pd.DataFrame(data, columns=['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
            'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms',
            'time_signature', 'key_none', 'key_0', 'key_1', 
            'key_2', 'key_3', 'key_4', 'key_5', 'key_6', 'key_7', 'key_8', 
            'key_9', 'key_10', 'key_11', 'mode_minor', 'mode_major','time_signature_0', 'time_signature_1',
            'time_signature_2', 'time_signature_3', 'time_signature_4', 'time_signature_5',
            'time_signature_6', 'time_signature_7'])
        user_playlist_model_data_df = user_playlist_data_df.copy()
        user_playlist_model_data_df = playlist_weight(user_playlist_model_data_df)
        user_playlist_model_data_df = user_playlist_model_data_df.drop(['key', 'mode', 'time_signature'], axis=1)

        # Scale the user playlist data, reform into a dataframe
        scaled_user_playlist_data = scaler.transform(user_playlist_model_data_df)
        scaled_user_playlist_data_df = pd.DataFrame(scaled_user_playlist_data,columns=user_playlist_model_data_df.columns, 
                                            index=user_playlist_model_data_df.index)

        # Make cluster prediction using the loaded model
        prediction = model.predict(scaled_user_playlist_data_df)

        # Isolate playlists within predicted cluster
        recommend_playlists = playlist_weight_df[playlist_weight_df["playlist_clusters"]==prediction[0]]

        # Use cosine similarity to find the 3 closest playlists to the user's playlist within the model
        recommend_playlists_df = recommend_playlists.drop(['playlist_clusters'],axis=1)
        recommend_playlists_df['similarity'] = cosine_similarity(recommend_playlists_df.values, scaled_user_playlist_data_df.values)
        recommend_playlists_df_top_3 = recommend_playlists_df.sort_values('similarity', ascending=False).head(3)
        recommend_playlists_df_top_3['pid'] = recommend_playlists_df_top_3.index

        # Gather track uri's from the 3 closest playlists, drop all other columns and remove duplicates
        recommended_df = pd.merge(recommend_playlists_df_top_3, playlist_ID_trackuri, on='pid')
        recommended_df = recommended_df[['pid','track_uri']]
        recommended_df.drop_duplicates(subset=['track_uri'])
        recommended_track_uri_df = recommended_df[['track_uri']]

        # Compare tracks in the 3 closest playlists to the users playlist to remove those already included
        recommended_track_uri_df = recommended_track_uri_df[~recommended_track_uri_df['track_uri'].isin(user_playist_track_uri)]
        recommended_track_list = list(recommended_track_uri_df['track_uri'])

        # Select 5 random songs from the remaining list
        random_selection = random.sample(range(1, len(recommended_track_list)), 5)
        output_recommendations = []
        for x in random_selection:
            output_recommendations.append(recommended_track_list[x])

        # Gather information from spotify on the 5 songs to recommend
        tracks_info = spotify.tracks(output_recommendations)

        # Compile recommended track data
        results = []
        for x in range(0,len(output_recommendations)):
            result_dict = {}
            result_dict['Track URI'] = tracks_info['tracks'][x]['uri']
            result_dict['Album Cover'] = tracks_info['tracks'][x]['album']['images'][0]['url']
            result_dict['Track Name'] = tracks_info['tracks'][x]['name']
            result_dict['Artist Name'] = tracks_info['tracks'][x]['artists'][0]['name']
            result_dict['Preview URL'] = tracks_info['tracks'][x]['preview_url']
            results.append(result_dict)

        return render_template('index.html', result1=results[0], result2=results[1], result3=results[2], result4=results[3], result5=results[4])

@app.route('/track_model_prediction', methods=['POST','GET'])
def track_model_prediction():
    if request.method == 'POST':
        # Extract input features from the request
        playlist_uri = str(request.form['track1'])

        # Load the model
        model_pkl_file = "mode_mean_7.pkl" 
        with open(model_pkl_file, 'rb') as file:  
            model = pickle.load(file)

        # Fit scaler to data without clusters
        scaler.fit(playlist_weight_df.drop('playlist_clusters',axis=1))

        # Establish a connection with the Spotify API
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

        # Gather all track URI's from the user's playlist
        user_playist_track_uri = []
        for i in range (0,1000,100):
            playlist_info = spotify.playlist_items('32tkDfEH8WuXiRqzREmWdX', offset=i, limit=100)
            for x in range(0,len(playlist_info['items'])):
                user_playist_track_uri.append(tracks_info['items'][x]['track']['uri'])
            if len(playlist_info['items']) < 100:
                break

        # Create a slice of 5 random tracks from the users playlist
        random_selection = random.sample(range(1, len(user_playist_track_uri)), 5)
        sample_uri_list = []
        for x in random_selection:
            sample_uri_list.append(user_playist_track_uri[x])

        # Request track data from spotify on the 5 track slice from the user playlist
        data=spotify.audio_features(sample_uri_list)

        # Create dummy variable cells for later input into the model
        key_to_add = ['key_none', 'key_0', 'key_1', 'key_2',
            'key_3', 'key_4', 'key_5', 'key_6', 'key_7', 'key_8', 'key_9', 'key_10',
            'key_11']
        mode_to_add = ['mode_minor', 'mode_major']
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

        # Create a datafram and edit column names and order to allow input to model
        user_playlist_data_df = pd.DataFrame(data, columns=['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
            'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms',
            'time_signature', 'key_none', 'key_0', 'key_1', 
            'key_2', 'key_3', 'key_4', 'key_5', 'key_6', 'key_7', 'key_8', 
            'key_9', 'key_10', 'key_11', 'mode_minor', 'mode_major'])
        user_playlist_data_model_df = user_playlist_data_df[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
            'duration_ms', 'time_signature', 'key_none', 'key_0', 'key_1', 
            'key_2', 'key_3', 'key_4', 'key_5', 'key_6', 'key_7', 'key_8', 
            'key_9', 'key_10', 'key_11', 'mode_minor', 'mode_major']]
        
        # Take the average of the playlist for use in the mean model
        user_playlist_data_model_mean_df = pd.DataFrame(user_playlist_data_model_df.mean()).transpose()
        user_playlist_data_model_mean_df = user_playlist_data_model_mean_df[['danceability', 'energy', 'key', 'key_none', 'key_0'
            'key_1', 'key_2', 'key_3', 'key_4','key_5', 'key_6', 
            'key_7', 'key_8', 'key_9', 'key_10', 'key_11', 
            'loudness', 'mode', 'mode_minor', 'mode_major', 
            'speechiness', 'acousticness', 'instrumentalness', 
            'liveness', 'valence', 'tempo', 'duration_ms',]]
        user_playlist_data_model_mean_df.columns=['mean_danceability', 'mean_energy', 'mean_key',
            'mean_key_none', 'mean_key_0', 'mean_key_1', 'mean_key_2', 'mean_key_3',
            'mean_key_4', 'mean_key_5', 'mean_key_6', 'mean_key_7', 'mean_key_8',
            'mean_key_9', 'mean_key_10', 'mean_key_11', 'mean_loudness',
            'mean_mode', 'mean_mode_minor', 'mean_mode_major', 'mean_speechiness',
            'mean_acousticness', 'mean_instrumentalness', 'mean_liveness',
            'mean_valence', 'mean_tempo', 'mean_duration_ms']
        
        # Scale the user playlist data, reform into a dataframe
        scaled_user_playlist_data_model_mean = scaler.transform(user_playlist_data_model_mean_df)
        scaled_user_playlist_data_model_mean_df = pd.DataFrame(scaled_user_playlist_data_model_mean,columns=user_playlist_data_model_mean_df.columns, index=user_playlist_data_model_mean_df.index)

        # Make cluster prediction using the loaded model
        prediction = model.predict(scaled_user_playlist_data_model_mean_df)

        # Isolate playlists within predicted cluster
        recommend_playlist = playlist_weight_df[playlist_weight_df["playlist_clusters"]==prediction[0]]

        # Use cosine similarity to find the 3 closest playlists to the user's playlist within the model
        recommend_playlists_df = recommend_playlist.drop(['playlist_clusters'],axis=1)
        recommend_playlists_df['similarity'] = cosine_similarity(recommend_playlists_df.values, scaled_user_playlist_data_model_mean_df.values)
        recommend_playlists_df_top_3 = recommend_playlists_df.sort_values('similarity', ascending=False).head(3)
        recommend_playlists_df_top_3['pid'] = recommend_playlists_df_top_3.index

        print(recommend_playlists_df_top_3)

        # Gather track uri's from the 3 closest playlists, drop all other columns and remove duplicates
        recommended_df = pd.merge(recommend_playlists_df_top_3, playlist_ID_trackuri, on='pid')
        recommended_df = recommended_df[['pid','track_uri']]
        recommended_df.drop_duplicates(subset=['track_uri'])
        recommended_track_uri_df = recommended_df[['track_uri']]

        # Compare tracks in the 3 closest playlists to the users playlist to remove those already included
        recommended_track_uri_df = recommended_track_uri_df[~recommended_track_uri_df['track_uri'].isin(user_playist_track_uri)]
        recommended_track_list = list(recommended_track_uri_df['track_uri'])

        print(recommended_track_list)

        # Select 5 random songs from the remaining list
        random_selection = random.sample(range(1, len(recommended_track_list)), 5)
        output_recommendations = []
        for x in random_selection:
            output_recommendations.append(recommended_track_list[x])

        # Gather information from spotify on the 5 songs to recommend
        tracks_info = spotify.tracks(output_recommendations)

        # Compile recommended track data
        results = []
        for x in range(0,len(output_recommendations)):
            result_dict = {}
            result_dict['Track URI'] = tracks_info['tracks'][x]['uri']
            result_dict['Album Cover'] = tracks_info['tracks'][x]['album']['images'][0]['url']
            result_dict['Track Name'] = tracks_info['tracks'][x]['name']
            result_dict['Artist Name'] = tracks_info['tracks'][x]['artists'][0]['name']
            result_dict['Preview URL'] = tracks_info['tracks'][x]['preview_url']
            results.append(result_dict)

        return render_template('index.html', result1=results[0], result2=results[1], result3=results[2], result4=results[3], result5=results[4])

@app.route('/mean_model_prediction', methods=['POST','GET'])
def mean_model_prediction():
    if request.method == 'POST':
        # Extract input features from the request
        playlist_uri = str(request.form['track1'])

        # Load the model
        model_pkl_file = "mode_mean_7.pkl" 
        with open(model_pkl_file, 'rb') as file:  
            model = pickle.load(file)

        # Fit scaler to data without clusters
        scaler.fit(playlist_weight_df.drop('playlist_clusters',axis=1))

        # Establish a connection with the Spotify API
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

        # Gather all track URI's from the user's playlist
        user_playist_track_uri = []
        for i in range (0,1000,100):
            playlist_info = spotify.playlist_items('32tkDfEH8WuXiRqzREmWdX', offset=i, limit=100)
            for x in range(0,len(playlist_info['items'])):
                user_playist_track_uri.append(tracks_info['items'][x]['track']['uri'])
            if len(playlist_info['items']) < 100:
                break

        # Create a slice of 5 random tracks from the users playlist
        random_selection = random.sample(range(1, len(user_playist_track_uri)), 5)
        sample_uri_list = []
        for x in random_selection:
            sample_uri_list.append(user_playist_track_uri[x])

        # Request track data from spotify on the 5 track slice from the user playlist
        data=spotify.audio_features(sample_uri_list)

        # Create dummy variable cells for later input into the model
        key_to_add = ['key_none', 'key_0', 'key_1', 'key_2',
            'key_3', 'key_4', 'key_5', 'key_6', 'key_7', 'key_8', 'key_9', 'key_10',
            'key_11']
        mode_to_add = ['mode_minor', 'mode_major']
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

        # Create a datafram and edit column names and order to allow input to model
        user_playlist_data_df = pd.DataFrame(data, columns=['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
            'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms',
            'time_signature', 'key_none', 'key_0', 'key_1', 
            'key_2', 'key_3', 'key_4', 'key_5', 'key_6', 'key_7', 'key_8', 
            'key_9', 'key_10', 'key_11', 'mode_minor', 'mode_major'])
        user_playlist_data_model_df = user_playlist_data_df[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
            'duration_ms', 'time_signature', 'key_none', 'key_0', 'key_1', 
            'key_2', 'key_3', 'key_4', 'key_5', 'key_6', 'key_7', 'key_8', 
            'key_9', 'key_10', 'key_11', 'mode_minor', 'mode_major']]
        
        # Take the average of the playlist for use in the mean model
        user_playlist_data_model_mean_df = pd.DataFrame(user_playlist_data_model_df.mean()).transpose()
        user_playlist_data_model_mean_df = user_playlist_data_model_mean_df[['danceability', 'energy', 'key', 'key_none', 'key_0'
            'key_1', 'key_2', 'key_3', 'key_4','key_5', 'key_6', 
            'key_7', 'key_8', 'key_9', 'key_10', 'key_11', 
            'loudness', 'mode', 'mode_minor', 'mode_major', 
            'speechiness', 'acousticness', 'instrumentalness', 
            'liveness', 'valence', 'tempo', 'duration_ms',]]
        user_playlist_data_model_mean_df.columns=['mean_danceability', 'mean_energy', 'mean_key',
            'mean_key_none', 'mean_key_0', 'mean_key_1', 'mean_key_2', 'mean_key_3',
            'mean_key_4', 'mean_key_5', 'mean_key_6', 'mean_key_7', 'mean_key_8',
            'mean_key_9', 'mean_key_10', 'mean_key_11', 'mean_loudness',
            'mean_mode', 'mean_mode_minor', 'mean_mode_major', 'mean_speechiness',
            'mean_acousticness', 'mean_instrumentalness', 'mean_liveness',
            'mean_valence', 'mean_tempo', 'mean_duration_ms']
        
        # Scale the user playlist data, reform into a dataframe
        scaled_user_playlist_data_model_mean = scaler.transform(user_playlist_data_model_mean_df)
        scaled_user_playlist_data_model_mean_df = pd.DataFrame(scaled_user_playlist_data_model_mean,columns=user_playlist_data_model_mean_df.columns, index=user_playlist_data_model_mean_df.index)

        # Make cluster prediction using the loaded model
        prediction = model.predict(scaled_user_playlist_data_model_mean_df)

        # Isolate playlists within predicted cluster
        recommend_playlist = playlist_weight_df[playlist_weight_df["playlist_clusters"]==prediction[0]]

        # Use cosine similarity to find the 3 closest playlists to the user's playlist within the model
        recommend_playlists_df = recommend_playlist.drop(['playlist_clusters'],axis=1)
        recommend_playlists_df['similarity'] = cosine_similarity(recommend_playlists_df.values, scaled_user_playlist_data_model_mean_df.values)
        recommend_playlists_df_top_3 = recommend_playlists_df.sort_values('similarity', ascending=False).head(3)
        recommend_playlists_df_top_3['pid'] = recommend_playlists_df_top_3.index

        print(recommend_playlists_df_top_3)

        # Gather track uri's from the 3 closest playlists, drop all other columns and remove duplicates
        recommended_df = pd.merge(recommend_playlists_df_top_3, playlist_ID_trackuri, on='pid')
        recommended_df = recommended_df[['pid','track_uri']]
        recommended_df.drop_duplicates(subset=['track_uri'])
        recommended_track_uri_df = recommended_df[['track_uri']]

        # Compare tracks in the 3 closest playlists to the users playlist to remove those already included
        recommended_track_uri_df = recommended_track_uri_df[~recommended_track_uri_df['track_uri'].isin(user_playist_track_uri)]
        recommended_track_list = list(recommended_track_uri_df['track_uri'])

        print(recommended_track_list)

        # Select 5 random songs from the remaining list
        random_selection = random.sample(range(1, len(recommended_track_list)), 5)
        output_recommendations = []
        for x in random_selection:
            output_recommendations.append(recommended_track_list[x])

        # Gather information from spotify on the 5 songs to recommend
        tracks_info = spotify.tracks(output_recommendations)

        # Compile recommended track data
        results = []
        for x in range(0,len(output_recommendations)):
            result_dict = {}
            result_dict['Track URI'] = tracks_info['tracks'][x]['uri']
            result_dict['Album Cover'] = tracks_info['tracks'][x]['album']['images'][0]['url']
            result_dict['Track Name'] = tracks_info['tracks'][x]['name']
            result_dict['Artist Name'] = tracks_info['tracks'][x]['artists'][0]['name']
            result_dict['Preview URL'] = tracks_info['tracks'][x]['preview_url']
            results.append(result_dict)

        return render_template('index.html', result1=results[0], result2=results[1], result3=results[2], result4=results[3], result5=results[4])

@app.route('/mean_model_precdition', methods=['POST','GET'])
def mean_model_precdition():
    if request.method == 'POST':
        # Extract input features from the request
        playlist_uri = str(request.form['track1'])

        # Load the model
        model_pkl_file = "mode_mean_7.pkl" 
        with open(model_pkl_file, 'rb') as file:  
            model = pickle.load(file)

        # Fit scaler to data without clusters
        scaler.fit(playlist_weight_df.drop('playlist_clusters',axis=1))

        # Establish a connection with the Spotify API
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

        # Gather all track URI's from the user's playlist
        user_playist_track_uri = []
        for i in range (0,1000,100):
            playlist_info = spotify.playlist_items('32tkDfEH8WuXiRqzREmWdX', offset=i, limit=100)
            for x in range(0,len(playlist_info['items'])):
                user_playist_track_uri.append(tracks_info['items'][x]['track']['uri'])
            if len(playlist_info['items']) < 100:
                break

        # Create a slice of 5 random tracks from the users playlist
        random_selection = random.sample(range(1, len(user_playist_track_uri)), 5)
        sample_uri_list = []
        for x in random_selection:
            sample_uri_list.append(user_playist_track_uri[x])

        # Request track data from spotify on the 5 track slice from the user playlist
        data=spotify.audio_features(sample_uri_list)

        # Create dummy variable cells for later input into the model
        key_to_add = ['key_none', 'key_0', 'key_1', 'key_2',
            'key_3', 'key_4', 'key_5', 'key_6', 'key_7', 'key_8', 'key_9', 'key_10',
            'key_11']
        mode_to_add = ['mode_minor', 'mode_major']
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

        # Create a datafram and edit column names and order to allow input to model
        user_playlist_data_df = pd.DataFrame(data, columns=['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
            'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms',
            'time_signature', 'key_none', 'key_0', 'key_1', 
            'key_2', 'key_3', 'key_4', 'key_5', 'key_6', 'key_7', 'key_8', 
            'key_9', 'key_10', 'key_11', 'mode_minor', 'mode_major'])
        user_playlist_data_model_df = user_playlist_data_df[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
            'duration_ms', 'time_signature', 'key_none', 'key_0', 'key_1', 
            'key_2', 'key_3', 'key_4', 'key_5', 'key_6', 'key_7', 'key_8', 
            'key_9', 'key_10', 'key_11', 'mode_minor', 'mode_major']]
        
        # Take the average of the playlist for use in the mean model
        user_playlist_data_model_mean_df = pd.DataFrame(user_playlist_data_model_df.mean()).transpose()
        user_playlist_data_model_mean_df = user_playlist_data_model_mean_df[['danceability', 'energy', 'key', 'key_none', 'key_0'
            'key_1', 'key_2', 'key_3', 'key_4','key_5', 'key_6', 
            'key_7', 'key_8', 'key_9', 'key_10', 'key_11', 
            'loudness', 'mode', 'mode_minor', 'mode_major', 
            'speechiness', 'acousticness', 'instrumentalness', 
            'liveness', 'valence', 'tempo', 'duration_ms',]]
        user_playlist_data_model_mean_df.columns=['mean_danceability', 'mean_energy', 'mean_key',
            'mean_key_none', 'mean_key_0', 'mean_key_1', 'mean_key_2', 'mean_key_3',
            'mean_key_4', 'mean_key_5', 'mean_key_6', 'mean_key_7', 'mean_key_8',
            'mean_key_9', 'mean_key_10', 'mean_key_11', 'mean_loudness',
            'mean_mode', 'mean_mode_minor', 'mean_mode_major', 'mean_speechiness',
            'mean_acousticness', 'mean_instrumentalness', 'mean_liveness',
            'mean_valence', 'mean_tempo', 'mean_duration_ms']
        
        # Scale the user playlist data, reform into a dataframe
        scaled_user_playlist_data_model_mean = scaler.transform(user_playlist_data_model_mean_df)
        scaled_user_playlist_data_model_mean_df = pd.DataFrame(scaled_user_playlist_data_model_mean,columns=user_playlist_data_model_mean_df.columns, index=user_playlist_data_model_mean_df.index)

        # Make cluster prediction using the loaded model
        prediction = model.predict(scaled_user_playlist_data_model_mean_df)

        # Isolate playlists within predicted cluster
        recommend_playlist = playlist_weight_df[playlist_weight_df["playlist_clusters"]==prediction[0]]

        # Use cosine similarity to find the 3 closest playlists to the user's playlist within the model
        recommend_playlists_df = recommend_playlist.drop(['playlist_clusters'],axis=1)
        recommend_playlists_df['similarity'] = cosine_similarity(recommend_playlists_df.values, scaled_user_playlist_data_model_mean_df.values)
        recommend_playlists_df_top_3 = recommend_playlists_df.sort_values('similarity', ascending=False).head(3)
        recommend_playlists_df_top_3['pid'] = recommend_playlists_df_top_3.index

        print(recommend_playlists_df_top_3)

        # Gather track uri's from the 3 closest playlists, drop all other columns and remove duplicates
        recommended_df = pd.merge(recommend_playlists_df_top_3, playlist_ID_trackuri, on='pid')
        recommended_df = recommended_df[['pid','track_uri']]
        recommended_df.drop_duplicates(subset=['track_uri'])
        recommended_track_uri_df = recommended_df[['track_uri']]

        # Compare tracks in the 3 closest playlists to the users playlist to remove those already included
        recommended_track_uri_df = recommended_track_uri_df[~recommended_track_uri_df['track_uri'].isin(user_playist_track_uri)]
        recommended_track_list = list(recommended_track_uri_df['track_uri'])

        print(recommended_track_list)

        # Select 5 random songs from the remaining list
        random_selection = random.sample(range(1, len(recommended_track_list)), 5)
        output_recommendations = []
        for x in random_selection:
            output_recommendations.append(recommended_track_list[x])

        # Gather information from spotify on the 5 songs to recommend
        tracks_info = spotify.tracks(output_recommendations)

        # Compile recommended track data
        results = []
        for x in range(0,len(output_recommendations)):
            result_dict = {}
            result_dict['Track URI'] = tracks_info['tracks'][x]['uri']
            result_dict['Album Cover'] = tracks_info['tracks'][x]['album']['images'][0]['url']
            result_dict['Track Name'] = tracks_info['tracks'][x]['name']
            result_dict['Artist Name'] = tracks_info['tracks'][x]['artists'][0]['name']
            result_dict['Preview URL'] = tracks_info['tracks'][x]['preview_url']
            results.append(result_dict)

        return render_template('index.html', result1=results[0], result2=results[1], result3=results[2], result4=results[3], result5=results[4])

# Run the Flask App locally
if __name__ == '__main__':
    app.run(debug=True)