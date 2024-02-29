# Jammin' With Spotify

## Introduction
In 2018, Spotify organized the [ACM RecSys Challenge 2018](https://www.recsyschallenge.com/2018/) in collaboration with the University of Massachusetts, Amherst, and the Johannes Kepler University, Linz. This challenge tried to crowd-source a solution for automatic playlist continuation by providing music recommendations. This challenged closed in July 2018, but Spotify sponsored in 2020 a similar challenge called the <b>Spotify Million Playlist Dataset Challenge</b>. For this challenge, Spotify made publicly available two curated datasets of 1,000,000 and 10,000 playlists respectively, made by US users of the Spotify platform between January 2010 and October 2017. The dataset is available on [AIcrowd](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge). The dataset of 1,000,000 playlists is to train the model, while the dataset of 10,000 playlists has missing tracks withheld by Spotify. The remaining tracks in the playlists have to be used as seeds by the model to make recommendations. The completed tracks are then sent to Spotify for comparison with the original complete playlists. The solutions are not made public by Spotify, so we cannot use this second dataset to test our model. We will then limit our model training to the first dataset of 1,000,000 playlists and validate our predictions by experimentations.<br>
Our goal is not to reverse engineer the song recommendation already available on Spotify, but to explore if song recommendations could be made based on only the musical characteristics of a track and without leveraging additional metadata such as the artist's name, the genre, or the popularity of tracks or of similar artists. 

## ETL pipe
Extraction and Transformation
The dataset consists of 1,000 json files, each containing 1,000 playlists.

<img src="https://github.com/JoeBrueneman/Jammin_With_Spotify/blob/Christophe/Images/original_json_file_structure.PNG" alt="Structure of the original json file" width="400">

The notebook <b><i>read_playlists.ipynb</i></b> reads through the 1,000 json files, extract the relevant data, and save the result into csv files to be imported into a database.
This process can take several hours, so another notebook <b><i>playlists_stats.ipynb</i></b> was developed to make lists of the unique tracks, unique artists, and unique albums present in the 1M-playlist dataset. This notebook runs in only 11min. Its code is adapted from a <b><i>stats.py</i></b> program provided by Spotify to verify the integrity of the dataset. It confirms that the dataset contains:
- number of playlists 1,000,000
- number of tracks 66,346,428
- number of unique tracks 2,262,292
- number of unique albums 734,684
- number of unique artists 295,860

The csv file containing the list of unique tracks is then read by a notebook <b><i>get_track_features_API.ipynb</i></b> which makes calls to the API made publicly available by Spotify and returns details (features) about the songs such as <i>danceability, energy, key, mode minor or major, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration_ms, and time_signature</i> (beats per bar). The details of the definitions can be found on the [Spotify website](https://developer.spotify.com/documentation/web-api/reference/get-audio-features).
Out of the 2,262,292 unique tracks present in the playlists, 47,300 do not return information about their features. They will be dropped from the analysis leaving us with feature information on 2,214,992 unique tracks.
A similar effort was made to collect the music genres associated with the artists <b><i>get_artist_genres.ipynb</i></b>, but it turns out that, out of the 295,860 unique artists present in the dataset, 171,825 of them do not have genre associated with them in the Spotify database. We will then not pursue this path further.

### Loading
The csv file with the feature information for the 2,214,992 unique tracks is loaded into a table in a PostgreSQL database.
<br><br>
<img src="https://github.com/JoeBrueneman/Jammin_With_Spotify/blob/Christophe/Images/track_feature_database.PNG" alt="View of the track feature table" width="900"> <br><br>
The <i>key</i> (0 = C, 1 = C♯/D♭, 2 = D, etc.), <i>mode</i> (minor or major), and <i>time response</i> (beats per bar) features have numerical values but are in fact categorical variables. We converted the information into dummy variables after importation with a PostgreSQL query rather than doing it with pandas prior to loading the data.
<br><br>
<img src="https://github.com/JoeBrueneman/Jammin_With_Spotify/blob/Christophe/Images/tracks_key_mode_dummies.PNG" alt="View of the dummy variables" width="900"> <br><br>

The playlist information is also loaded in a table. Since each track has its own row, the table has 66,346,428 rows, which matches the statistics measured from the raw json files.
<br><br>
<img src="https://github.com/JoeBrueneman/Jammin_With_Spotify/blob/Christophe/Images/playlist_database.PNG" alt="View of the playlist table" width="900"> <br><br>
#### ERD
The two tables can be linked by the <i>track_uri</i> parameter.<br><br>
<img src="https://github.com/JoeBrueneman/Jammin_With_Spotify/blob/Christophe/Images/database_ERD.PNG" alt="View of the playlist table" width="400"> <br><br>

### Joining Tables
In preparation for the clusterization of the data, we experimented two approaches:
- Approach 1: We summarize each individual playlist by averaging the numerical values of the features over all the tracks it contains. Note that the mean value of the key, the mode, and the time response features have no meaning and will be excluded from the model. In lieu of the mean, the statistical mode of the feature is reported in the corresponding dummy variable making the value a representation of the most common keys, time response, and the minor or major modes present in the playlist. This approach is used when comparing a playlist directly with the tracks in the database.
  <br><br>
  <img src="https://github.com/JoeBrueneman/Jammin_With_Spotify/blob/Christophe/Images/View_mean.PNG" alt="View of the joined tables with averages" width="900"> <br><br>
- Approach 2: A limitation of the first approach is that the mathematical averages hide the distribution for the features. A narrow distribution could mean that the user consciously or unconsciously gave a higher importance for this feature. We supplemented the number of features by adding the standard deviation of all the continuous variables for each playlist. A smaller standard deviation will reinforce the importance of the feature for the owner of the playlist, and will play in the clusterization. This approach is used when comparing a playlist with other playlists from the same cluster.
  <br><br>
  <img src="https://github.com/JoeBrueneman/Jammin_With_Spotify/blob/Christophe/Images/View_weights.PNG" alt="View of the joined tables with weighted averages" width="900"> <br><br>

#### Remark about the Spotify data:
The terms and conditions defined by Spotify to use this dataset are very restrictive. In particular, Spotify doesn’t allow to “<i>[…] sell, rent, transfer, distribute, make available, or otherwise disclose Spotify Data […]</i>”, therefore we will not save the data collected on Github or make the database available to people outside of this project group. The database and the associated files will be deleted by the end of this class (2/29/2024).





## References
C.W. Chen, P. Lamere, M. Schedl, and H. Zamani. Recsys Challenge 2018: Automatic Music Playlist Continuation. In Proceedings of the 12th ACM Conference on Recommender Systems (RecSys ’18), 2018. 



