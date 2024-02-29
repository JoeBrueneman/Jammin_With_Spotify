# Jamming_With_Spotify - Model Section


##  Comparable Study Of Different Models

* We conduct four different ways of approach to recommend new tracks given a user input playlist, the following flow charts shows the logic behind it:
![model_flow](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/18a7bbe6-a5d4-475f-b972-9595867953e2)

* We build three models to perform the recommendation task:
  * A cosine-similarity model that compare the input playlist vector to all the track vectors;
  * A track-clustering model that cluster all the tracks, then comparing the input playlist vector, after labeling, to all the same cluster of tracks;
  * A playlist-wm-clustering model that cluster all the weighted-mean of the playlists audio features, then comparing the input playlist vector, after labeling, to all the same cluster of playlists.

## Model Architecture
* Model 1: Cosine-Similarity\
  Is a method used to evaluate similarity of vectors by calculating the cosine of their angles. In our case, we compare a user’s playlist vector to all the song vectors in our database. The features we use for formulating the vectors are audio features, such as loudness, energy, acoustics, instrumentalness, liveness, etc.. We rank the similarity values of each track by a descending order and recommend the top ones to the user.
![cosine_flow](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/866c4ebf-d1ae-4f59-99f0-b8f8deb28527)


* Model 2: Track-Clustering\
  In recommendation systems, clustering algorithms can be used to group similar items together based on their features. In content-based filtering for tracks, we implement this method to group similar tracks together. We then assign a cluster number to the input playlist by aggregating its features and recommend tracks from the same cluster.
![track_flow](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/d8f201f7-8735-4e49-965a-8bc83e6d0f94)


* Model 4: Playlist-Clustering\
  In recommendation systems, clustering algorithms can be used to group similar users together based on their preferences and behaviors. We assume that the creation of a playlist implies the user’s song preferences and grouping behavior. By grouping similar playlists together and assigning the input playlist to a cluster, we recommend songs from other similar playlists from the same cluster to the user.
![playlist_flow](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/f6a33a97-9db3-4d98-b99d-5387a4f30511)

## Training Data
Please refer to 'Data Pipe' in previous section.

## Visualization
* Track clustering with 17 clusters\
  By running the 'Elbow Method' and TSNE visualization (see jupyter notebook file for details), we set cluster number for tracks equals to 17, and the visualiztion is shown below:

![image](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/bedaf4d4-136b-44a2-a01d-a139cc3cc519)
  

* Playlist clustering with 18 clusters\
  By running the 'Elbow Method' and TSNE visualization (see jupyter notebook file for details), we set cluster number playlists equals to 18, and the visualiztion is shown below:
  
![image](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/55eadf73-10f4-4624-99dc-f1687a92b0ce)


## Validation Method

We take a playlist dataset as test sample and split it into train (80%) and test (20%) datasets, named 'feed' and 'validate'. We generate a 'predict' dataset by using the 'feed' dataset witht the three models above. Then we compare the similarity of the 'predict' dataset to 'validate' dataset and calculate the accuracy. 

## Acknowledgments

A group collaboration of:\
Christophe Vivensang\
Gia Liu\
Joe Brueneman\
Julia Min\
Minh Le\

and special thanks to:\
Lisa\
Shannon


