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
The <i>key</i> (0 = C, 1 = C♯/D♭, 2 = D, etc.), <i>mode</i> (minor or major), and <i>time signature</i> (beats per bar) features have numerical values but are in fact categorical variables. We converted the information into dummy variables after importation with a PostgreSQL query rather than doing it with pandas prior to loading the data.
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
- Approach 1: We summarize each individual playlist by averaging the numerical values of the features over all the tracks it contains. Note that the mean value of the key, the mode, and the time signature features have no meaning and will be excluded from the model. In lieu of the mean, the statistical mode of the feature is reported in the corresponding dummy variable making the value a representation of the most common key, time signature, and the minor or major mode present in the playlist. This approach is used when comparing a playlist directly with the tracks in the database.
  <br><br>
  <img src="https://github.com/JoeBrueneman/Jammin_With_Spotify/blob/Christophe/Images/View_mean.PNG" alt="View of the joined tables with averages" width="900"> <br><br>
- Approach 2: A limitation of the first approach is that the mathematical averages hide the distribution for the features. A narrow distribution could mean that the user consciously or unconsciously gave a higher importance for this feature. We supplemented the number of features by adding the standard deviation of all the continuous variables for each playlist. A smaller standard deviation will reinforce the importance of the feature for the owner of the playlist, and will play in the clusterization. This approach is used when comparing a playlist with other playlists from the same cluster.
  <br><br>
  <img src="https://github.com/JoeBrueneman/Jammin_With_Spotify/blob/Christophe/Images/View_weights.PNG" alt="View of the joined tables with weighted averages" width="900"> <br><br>

##  Comparable Study Of Different Models

* We conduct three different ways of approach to recommend new tracks given a user input playlist, the following flow charts shows the logic behind it:
![model_flow](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/18a7bbe6-a5d4-475f-b972-9595867953e2)

* We build three models to perform the recommendation task:
  * A cosine-similarity model that compare the input playlist vector to all the track vectors;
  * A track-clustering model that clusters all the tracks, then comparing the input playlist vector, after labeling, to all the same cluster of tracks;
  * A playlist-clustering model that clusters all the weighted-mean of the playlists audio features, then comparing the input playlist vector, after labeling, to all the same cluster of playlists.

## Model Architecture
* Model 1: Cosine-Similarity\
  Is a method used to evaluate similarity of vectors by calculating the cosine of their angles. In our case, we compare a user’s playlist vector to all the song vectors in our database. The features we use for formulating the vectors are audio features, such as loudness, energy, acoustics, instrumentalness, liveness, etc.. We rank the similarity values of each track by a descending order and recommend the top ones to the user.
![cosine_flow](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/866c4ebf-d1ae-4f59-99f0-b8f8deb28527)


* Model 2: Track-Clustering\
  In recommendation systems, clustering algorithms can be used to group similar items together based on their features. In content-based filtering for tracks, we implement this method to group similar tracks together. We then assign a cluster number to the input playlist by aggregating its features and recommend tracks from the same cluster.
![track_cluster](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/82e7bf7c-e2f7-4765-9142-9e82f7088ae9)



* Model 3: Playlist-Clustering\
  In recommendation systems, clustering algorithms can be used to group similar users together based on their preferences and behaviors. We assume that the creation of a playlist implies the user’s song preferences and grouping behavior. By grouping similar playlists together and assigning the input playlist to a cluster, we recommend songs from other similar playlists from the same cluster to the user.
![playlist cluster](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/6467a5c2-f90e-4393-bd52-edbce47f0aa8)


## Training Data
Please refer to 'Data Pipe' in previous section.

## Visualization
* Track clustering with 17 clusters\
  By running the 'Elbow Method' and TSNE visualization (see jupyter notebook file for details), we set cluster number for tracks equals to 17, and the visualization is shown below:
  
  ![track_clusters_K17_transparent](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/cd7579da-54f6-46cc-9385-21992c6f5e72)


* Playlist clustering with 17 clusters\
  By running the 'Elbow Method' and TSNE visualization (see jupyter notebook file for details), we set cluster number playlists equals to 17, and the visualization is shown below:
  
![image](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/bedaf4d4-136b-44a2-a01d-a139cc3cc519)


## Validation Method

We take a playlist dataset as test sample and split it into train (80%) and test (20%) datasets, named 'feed' and 'validate'. We generate a 'predict' dataset by using the 'feed' dataset witht the three models above. Then we compare the similarity of the 'predict' dataset to 'validate' dataset and calculate the accuracy. 


## Website

The 'Jammin' with Spotify' website is a responsive and innovative platform designed to explore musical tastes and suggest a variety of songs from a database of a million Spotify playlists. It provides clear instructions for users on how to test out the model. By inputting a Spotify playlist URI, the machine learning model assesses musical preferences to recommend five personalized songs, complete with brief previews for immediate listening. Developed from analyzing data across 1 million Spotify playlists, this tool not only showcases a method of song recommendation through technology but also offers insights into our approach. These insights, based on three distinct approaches to data analysis, are accessible in the 'Statistics' section, enhancing user understanding of the underlying processes.

## Acknowledgments

A group collaboration of:\
Christophe Vivensang\
Gia Liu\
Joe Brueneman\
Julia Min\
Minh Le

and special thanks to:\
Khaled Karman\
Jin Park\
Brian Perry\
Karen Fisher\
Lisa\
Shannon







#### Remark about the Spotify data:
The terms and conditions defined by Spotify to use this dataset are very restrictive. In particular, Spotify doesn’t allow to “<i>[…] sell, rent, transfer, distribute, make available, or otherwise disclose Spotify Data […]</i>”, therefore we will not save the data collected on Github or make the database available to people outside of this project group. The database and the associated files will be deleted by the end of this class (2/29/2024).





## References
C.W. Chen, P. Lamere, M. Schedl, and H. Zamani. Recsys Challenge 2018: Automatic Music Playlist Continuation. In Proceedings of the 12th ACM Conference on Recommender Systems (RecSys ’18), 2018. 



