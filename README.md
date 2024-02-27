# Jamming_With_Spotify - Model Section


##  Comparable Study Of Different Models

* We conduct four different ways of approach to recommend new tracks given a user input playlist, the following flow charts shows the logic behind it:
![MODEL-FLOW](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/66d13ea1-1b66-4a46-a780-e7987c6404ad)

* We build four models to perform the recommendation task:
  * A cosine-similarity model that compare the input playlist vector to all the track vectors;
  * A track-clustering model that cluster all the tracks, then comparing the input playlist vector, after labeling, to all the same cluster of tracks;
  * A playlist-m-clustering model that cluster all the mean of the playlists audio features, then comparing the input playlist vector, after labeling, to all the same cluster of playlists;
  * A playlist-wm-clustering model that cluster all the weighted-mean of the playlists audio features, then comparing the input playlist vector, after labeling, to all the same cluster of playlists.

## Model Architecture
* Model 1: Cosine-Similarity
![Slide2](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/bae80af8-3782-46bd-b7f2-414e763b7778)

* Model 2: Track-Clustering
![Slide3](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/35562536-bb5d-41ee-8560-240df8658ed9)

* Model 3: Playlist-Clustering with mean aggregation
![Slide4](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/ab2bba40-f2b4-46f6-bc49-9850e901b743)

* Model 4: Playlist-Clustering with weighted-mean aggregation
![Slide5](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/aa0808de-df0c-4a5c-898f-124f24c64aa3)

## Training Data
Please refer to 'Data Pipe' in previous section.

## Visualization
* Track clustering with 11 clusters
  
![track_cluster_11](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/248b91b1-3a16-4ec8-8a5b-ab67c56b9754)

* Playlist clustering

![Slide1](https://github.com/JoeBrueneman/Jammin_With_Spotify/assets/141379548/22de6020-80ec-4903-b7d0-a158f009bb5e)




## Evaluation Metrics

Explanation of the evaluation metrics used to assess model performance.

## Results

Presentation of model evaluation results.

## Acknowledgments

Give credit to any individuals or resources that contributed to the project.
