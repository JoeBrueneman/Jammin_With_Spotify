-- List of queries used to transform the PostgreSQL tables


-- Creation of the initial tables

CREATE TABLE "track_features" (
    "danceability" FLOAT   NOT NULL,
    "energy" FLOAT   NOT NULL,
    "key" INT   NOT NULL,
    "key_none" INT,
    "key_0" INT,
    "key_1" INT,
    "key_2" INT,
    "key_3" INT,
    "key_4" INT,
    "key_5" INT,
    "key_6" INT,
    "key_7" INT,
    "key_8" INT,
    "key_9" INT,
    "key_10" INT,
    "key_11" INT,
    "loudness" FLOAT   NOT NULL,
    "mode" INT   NOT NULL,
    "mode_minor" INT,
    "mode_major" INT,
    "speechiness" FLOAT   NOT NULL,
    "acousticness" FLOAT   NOT NULL,
    "instrumentalness" FLOAT   NOT NULL,
    "liveness" FLOAT   NOT NULL,
    "valence" FLOAT   NOT NULL,
    "tempo" FLOAT   NOT NULL,
    "id" VARCHAR(50)   NOT NULL,
    "track_uri" VARCHAR(70)   NOT NULL,
    "track_href" VARCHAR(70)   NOT NULL,
    "analysis_url" VARCHAR(100)   NOT NULL,
    "duration_ms" INT   NOT NULL,
    "time_signature" INT   NOT NULL,
    CONSTRAINT "pk_track_features" PRIMARY KEY (
        "track_uri"
     )
);

CREATE TABLE "playlist" (
    "pid" INT   NOT NULL,
    "name" VARCHAR(200),
    "num_tracks" INT   NOT NULL,
    "pos" INT   NOT NULL,
    "track_name" VARCHAR(400),
    "track_uri" VARCHAR(70)   NOT NULL,
    "artist_name" VARCHAR(400),
    "artist_uri" VARCHAR(70)   NOT NULL,
    "album_name" VARCHAR(400),
    "album_uri" VARCHAR(70)   NOT NULL,
    "duration_ms" INT   NOT NULL
);

-- Modification of the track_features table to add the dummy variables key and mode
ALTER TABLE IF EXISTS public.track_features
  	ADD COLUMN mode_minor integer DEFAULT 0,
	ADD COLUMN mode_major integer DEFAULT 0;
	
	
UPDATE track_features
SET mode_minor = 
	CASE WHEN "mode"=0
		THEN 1
		ELSE 0
	END;
	
UPDATE track_features
SET mode_major = 
	CASE WHEN "mode"=1
		THEN 1
		ELSE 0
	END;
	

UPDATE track_features
SET key_none = 
	CASE WHEN "key"=-1
		THEN 1
		ELSE 0
	END;
	
UPDATE track_features
SET key_0 = 
	CASE WHEN "key"=0
		THEN 1
		ELSE 0
	END;
	
UPDATE track_features
SET key_1 = 
	CASE WHEN "key"=1
		THEN 1
		ELSE 0
	END;
	
UPDATE track_features
SET key_2 = 
	CASE WHEN "key"=2
		THEN 1
		ELSE 0
	END;
	
UPDATE track_features
SET key_3 = 
	CASE WHEN "key"=3
		THEN 1
		ELSE 0
	END;
	
UPDATE track_features
SET key_4 = 
	CASE WHEN "key"=4
		THEN 1
		ELSE 0
	END;
	
UPDATE track_features
SET key_5 = 
	CASE WHEN "key"=5
		THEN 1
		ELSE 0
	END;
	
UPDATE track_features
SET key_6 = 
	CASE WHEN "key"=6
		THEN 1
		ELSE 0
	END;
	
UPDATE track_features
SET key_7 = 
	CASE WHEN "key"=7
		THEN 1
		ELSE 0
	END;
	
UPDATE track_features
SET key_8 = 
	CASE WHEN "key"=8
		THEN 1
		ELSE 0
	END;
	
UPDATE track_features
SET key_9 = 
	CASE WHEN "key"=9
		THEN 1
		ELSE 0
	END;
	
UPDATE track_features
SET key_10 = 
	CASE WHEN "key"=10
		THEN 1
		ELSE 0
	END;
	
UPDATE track_features
SET key_11 = 
	CASE WHEN "key"=11
		THEN 1
		ELSE 0
	END;

SELECT "key", key_none, key_0, key_1, key_2, key_3, key_4, key_5, key_6, key_7, key_8, key_9, key_10, key_11, "mode", mode_minor, mode_major
FROM track_features


-- Creation of the relationship between the two tables
ALTER TABLE "track_features" ADD CONSTRAINT "fk_track_features_track_uri" FOREIGN KEY("track_uri")
REFERENCES "playlist" ("track_uri");


-- Creation of the VIEW  playlist_stat_mean (Approach 1)
DROP VIEW IF EXISTS playlist_stat_mean;
CREATE VIEW playlist_stat_mean AS 
SELECT playlist.pid, COUNT(*) AS tracks_found, AVG(track_features.danceability) AS mean_danceability, AVG(track_features.energy) AS mean_energy, AVG(track_features.key) AS mean_key,
					SUM(track_features.key_none) / COUNT(*) AS mean_key_none,
					SUM(track_features.key_0 ::FLOAT) / COUNT(*) AS mean_key_0,
					SUM(track_features.key_1 ::FLOAT) / COUNT(*) AS mean_key_1,
					SUM(track_features.key_2 ::FLOAT) / COUNT(*) AS mean_key_2,
					SUM(track_features.key_3 ::FLOAT) / COUNT(*) AS mean_key_3,
					SUM(track_features.key_4 ::FLOAT) / COUNT(*) AS mean_key_4,
					SUM(track_features.key_5 ::FLOAT) / COUNT(*) AS mean_key_5,
					SUM(track_features.key_6 ::FLOAT) / COUNT(*) AS mean_key_6,
					SUM(track_features.key_7 ::FLOAT) / COUNT(*) AS mean_key_7,
					SUM(track_features.key_8 ::FLOAT) / COUNT(*) AS mean_key_8,
					SUM(track_features.key_9 ::FLOAT) / COUNT(*) AS mean_key_9,
					SUM(track_features.key_10 ::FLOAT) / COUNT(*) AS mean_key_10,
					SUM(track_features.key_11 ::FLOAT) / COUNT(*) AS mean_key_11,
					AVG(track_features.loudness) AS mean_loudness,
					AVG(track_features.mode) AS mean_mode,
					SUM(track_features.mode_minor ::FLOAT) / COUNT(*) AS mean_mode_minor,
					SUM(track_features.mode_major ::FLOAT) / COUNT(*) AS mean_mode_major,
					AVG(track_features.speechiness) AS mean_speechiness, AVG(track_features.acousticness) AS mean_acousticness, AVG(track_features.instrumentalness) AS mean_instrumentalness,
					AVG(track_features.liveness) AS mean_liveness, AVG(track_features.valence) AS mean_valence, AVG(track_features.tempo) AS mean_tempo,
					AVG(track_features.duration_ms) AS mean_duration_ms
		
FROM playlist
INNER JOIN track_features
ON playlist.track_uri = track_features.track_uri
GROUP BY playlist.pid
ORDER BY playlist.pid;


SELECT * FROM playlist_stat_mean


-- Creation of the VIEW  playlist_stat_weights (Approach 2)
DROP VIEW IF EXISTS playlist_stat_weights;
CREATE VIEW playlist_stat_weights AS 
SELECT playlist.pid, COUNT(*) AS tracks_found,
	AVG(track_features.danceability) / STDDEV(track_features.danceability) AS weight_danceability,
	AVG(track_features.energy) / STDDEV(track_features.energy) AS weight_energy,
	AVG(track_features.key) AS mean_key,
	SUM(track_features.key_none) / COUNT(*) AS mean_key_none,
	SUM(track_features.key_0 ::FLOAT) / COUNT(*) AS proportion_key_0,
	SUM(track_features.key_1 ::FLOAT) / COUNT(*) AS proportion_key_1,
	SUM(track_features.key_2 ::FLOAT) / COUNT(*) AS proportion_key_2,
	SUM(track_features.key_3 ::FLOAT) / COUNT(*) AS proportion_key_3,
	SUM(track_features.key_4 ::FLOAT) / COUNT(*) AS proportion_key_4,
	SUM(track_features.key_5 ::FLOAT) / COUNT(*) AS proportion_key_5,
	SUM(track_features.key_6 ::FLOAT) / COUNT(*) AS proportion_key_6,
	SUM(track_features.key_7 ::FLOAT) / COUNT(*) AS proportion_key_7,
	SUM(track_features.key_8 ::FLOAT) / COUNT(*) AS proportion_key_8,
	SUM(track_features.key_9 ::FLOAT) / COUNT(*) AS proportion_key_9,
	SUM(track_features.key_10 ::FLOAT) / COUNT(*) AS proportion_key_10,
	SUM(track_features.key_11 ::FLOAT) / COUNT(*) AS proportion_key_11,
	AVG(track_features.loudness) / STDDEV(track_features.loudness) AS weight_loudness,
	AVG(track_features.mode) AS mean_mode,
	SUM(track_features.mode_minor ::FLOAT) / COUNT(*) AS proportion_mode_minor,
	SUM(track_features.mode_major ::FLOAT) / COUNT(*) AS proportion_mode_major,
	AVG(track_features.speechiness) / STDDEV(track_features.speechiness) AS weight_speechiness,
	AVG(track_features.acousticness) / STDDEV(track_features.acousticness) AS weight_acousticness,
	
	AVG(track_features.instrumentalness)/(
		CASE WHEN STDDEV(track_features.instrumentalness)=0 -- Remark: There are 1796 playlists in the dataset having individually the same instrumentalness value across their tracks.
			THEN 0.00000013                                 -- To avoid a "division by zero" error, we arbitrary replace the stddev by 1.3e-7 which slighly less than the smallest non-null stddev for this feature.
			ELSE STDDEV(track_features.instrumentalness)
		END
		) AS weight_instrumentalness,	
	
	AVG(track_features.liveness) / STDDEV(track_features.liveness) AS weight_liveness,
	AVG(track_features.valence) / STDDEV(track_features.valence) AS weight_valence,
	AVG(track_features.tempo) / STDDEV(track_features.tempo) AS weight_tempo,
	AVG(track_features.duration_ms) / STDDEV(track_features.duration_ms) AS weight_duration_ms
			
FROM playlist
INNER JOIN track_features
ON playlist.track_uri = track_features.track_uri
GROUP BY playlist.pid
ORDER BY playlist.pid;

SELECT * FROM playlist_stat_weights;

--
-- Creation of the VIEW  playlist_stat_mean_mode, which is a modification of Approach 1 to show the statistical mode of the features key and mode for each playlist
DROP VIEW IF EXISTS playlist_stat_mean_mode;
CREATE VIEW playlist_stat_mean_mode AS 
SELECT playlist.pid, COUNT(*) AS tracks_found, AVG(track_features.danceability) AS mean_danceability, AVG(track_features.energy) AS mean_energy,
                    MODE () WITHIN GROUP ( ORDER BY "key" ) AS mode_key,
					SUM(track_features.key_none) / COUNT(*) AS mean_key_none,
					SUM(track_features.key_0 ::FLOAT) / COUNT(*) AS mean_key_0,
					SUM(track_features.key_1 ::FLOAT) / COUNT(*) AS mean_key_1,
					SUM(track_features.key_2 ::FLOAT) / COUNT(*) AS mean_key_2,
					SUM(track_features.key_3 ::FLOAT) / COUNT(*) AS mean_key_3,
					SUM(track_features.key_4 ::FLOAT) / COUNT(*) AS mean_key_4,
					SUM(track_features.key_5 ::FLOAT) / COUNT(*) AS mean_key_5,
					SUM(track_features.key_6 ::FLOAT) / COUNT(*) AS mean_key_6,
					SUM(track_features.key_7 ::FLOAT) / COUNT(*) AS mean_key_7,
					SUM(track_features.key_8 ::FLOAT) / COUNT(*) AS mean_key_8,
					SUM(track_features.key_9 ::FLOAT) / COUNT(*) AS mean_key_9,
					SUM(track_features.key_10 ::FLOAT) / COUNT(*) AS mean_key_10,
					SUM(track_features.key_11 ::FLOAT) / COUNT(*) AS mean_key_11,
					AVG(track_features.loudness) AS mean_loudness,
					MODE () WITHIN GROUP ( ORDER BY "mode" ) AS mode_mode,
					SUM(track_features.mode_minor ::FLOAT) / COUNT(*) AS mean_mode_minor,
					SUM(track_features.mode_major ::FLOAT) / COUNT(*) AS mean_mode_major,
					AVG(track_features.speechiness) AS mean_speechiness, AVG(track_features.acousticness) AS mean_acousticness, AVG(track_features.instrumentalness) AS mean_instrumentalness,
					AVG(track_features.liveness) AS mean_liveness, AVG(track_features.valence) AS mean_valence, AVG(track_features.tempo) AS mean_tempo,
					AVG(track_features.duration_ms) AS mean_duration_ms
		
FROM playlist
INNER JOIN track_features
ON playlist.track_uri = track_features.track_uri
GROUP BY playlist.pid
ORDER BY playlist.pid;


SELECT * FROM playlist_stat_mean_mode


-- Creation of the VIEW  playlist_stat_weight_mode, which is a modification of Approach 2 to show the statistical mode of the features key and mode for each playlist
DROP VIEW IF EXISTS playlist_stat_weight_mode;
CREATE VIEW playlist_stat_weight_mode AS 
SELECT playlist.pid, COUNT(*) AS tracks_found,
	AVG(track_features.danceability) / STDDEV(track_features.danceability) AS weight_danceability,
	AVG(track_features.energy) / STDDEV(track_features.energy) AS weight_energy,
	MODE () WITHIN GROUP ( ORDER BY "key" ) AS mode_key,
	SUM(track_features.key_none ::FLOAT) / COUNT(*) AS proportion_key_none,	
	SUM(track_features.key_0 ::FLOAT) / COUNT(*) AS proportion_key_0,
	SUM(track_features.key_1 ::FLOAT) / COUNT(*) AS proportion_key_1,
	SUM(track_features.key_2 ::FLOAT) / COUNT(*) AS proportion_key_2,
	SUM(track_features.key_3 ::FLOAT) / COUNT(*) AS proportion_key_3,
	SUM(track_features.key_4 ::FLOAT) / COUNT(*) AS proportion_key_4,
	SUM(track_features.key_5 ::FLOAT) / COUNT(*) AS proportion_key_5,
	SUM(track_features.key_6 ::FLOAT) / COUNT(*) AS proportion_key_6,
	SUM(track_features.key_7 ::FLOAT) / COUNT(*) AS proportion_key_7,
	SUM(track_features.key_8 ::FLOAT) / COUNT(*) AS proportion_key_8,
	SUM(track_features.key_9 ::FLOAT) / COUNT(*) AS proportion_key_9,
	SUM(track_features.key_10 ::FLOAT) / COUNT(*) AS proportion_key_10,
	SUM(track_features.key_11 ::FLOAT) / COUNT(*) AS proportion_key_11,
	AVG(track_features.loudness) / STDDEV(track_features.loudness) AS weight_loudness,
	MODE () WITHIN GROUP ( ORDER BY "mode" ) AS mode_mode,
	SUM(track_features.mode_minor ::FLOAT) / COUNT(*) AS proportion_mode_minor,
	SUM(track_features.mode_major ::FLOAT) / COUNT(*) AS proportion_mode_major,
	AVG(track_features.speechiness) / STDDEV(track_features.speechiness) AS weight_speechiness,
	AVG(track_features.acousticness) / STDDEV(track_features.acousticness) AS weight_acousticness,
	AVG(track_features.instrumentalness)/(
		CASE WHEN STDDEV(track_features.instrumentalness)=0 -- Remark: There are 1796 playlists in the dataset having individually the same instrumentalness value across their tracks.
			THEN 0.00000013                                 -- To avoid a "division by zero" error, we arbitrary replace the stddev by 1.3e-7 which slighly less than the smallest non-null stddev for this feature.
			ELSE STDDEV(track_features.instrumentalness)
		END
		) AS weight_instrumentalness,	
	
	AVG(track_features.liveness) / STDDEV(track_features.liveness) AS weight_liveness,
	AVG(track_features.valence) / STDDEV(track_features.valence) AS weight_valence,
	AVG(track_features.tempo) / STDDEV(track_features.tempo) AS weight_tempo,
	AVG(track_features.duration_ms) / STDDEV(track_features.duration_ms) AS weight_duration_ms
			
FROM playlist
INNER JOIN track_features
ON playlist.track_uri = track_features.track_uri
GROUP BY playlist.pid
ORDER BY playlist.pid;

SELECT * FROM playlist_stat_weight_mode;

--*

ALTER TABLE IF EXISTS public.track_features
  	ADD COLUMN time_signature_0 integer DEFAULT 0,
	ADD COLUMN time_signature_1 integer DEFAULT 0,
  	ADD COLUMN time_signature_2 integer DEFAULT 0,
	ADD COLUMN time_signature_3 integer DEFAULT 0,	
  	ADD COLUMN time_signature_4 integer DEFAULT 0,
	ADD COLUMN time_signature_5 integer DEFAULT 0,
	ADD COLUMN time_signature_6 integer DEFAULT 0,	
  	ADD COLUMN time_signature_7 integer DEFAULT 0;
	
	

UPDATE track_features
SET time_signature_0 = 
	CASE WHEN time_signature=0
		THEN 1
		ELSE 0
	END;

    -- *****************
	
    -- *********

DROP VIEW IF EXISTS playlist_stat_mean_mode;
CREATE VIEW playlist_stat_mean_mode AS 
SELECT playlist.pid, COUNT(*) AS tracks_found,
					AVG(track_features.danceability) AS danceability,
					AVG(track_features.energy) AS energy,
					AVG(track_features.loudness) AS loudness,
					AVG(track_features.speechiness) AS speechiness,
					AVG(track_features.acousticness) AS acousticness,
					AVG(track_features.instrumentalness) AS instrumentalness,
					AVG(track_features.liveness) AS liveness,
					AVG(track_features.valence) AS valence,
					AVG(track_features.tempo) AS tempo,
					AVG(track_features.duration_ms) AS duration_ms,

                    MODE () WITHIN GROUP ( ORDER BY "key" ) AS mode_key,
					SUM(track_features.key_none) / COUNT(*) AS key_none,
					SUM(track_features.key_0 ::FLOAT) / COUNT(*) AS key_0,
					SUM(track_features.key_1 ::FLOAT) / COUNT(*) AS key_1,
					SUM(track_features.key_2 ::FLOAT) / COUNT(*) AS key_2,
					SUM(track_features.key_3 ::FLOAT) / COUNT(*) AS key_3,
					SUM(track_features.key_4 ::FLOAT) / COUNT(*) AS key_4,
					SUM(track_features.key_5 ::FLOAT) / COUNT(*) AS key_5,
					SUM(track_features.key_6 ::FLOAT) / COUNT(*) AS key_6,
					SUM(track_features.key_7 ::FLOAT) / COUNT(*) AS key_7,
					SUM(track_features.key_8 ::FLOAT) / COUNT(*) AS key_8,
					SUM(track_features.key_9 ::FLOAT) / COUNT(*) AS key_9,
					SUM(track_features.key_10 ::FLOAT) / COUNT(*) AS key_10,
					SUM(track_features.key_11 ::FLOAT) / COUNT(*) AS key_11,

					MODE () WITHIN GROUP ( ORDER BY "mode" ) AS mode,
					SUM(track_features.mode_minor ::FLOAT) / COUNT(*) AS mode_minor,
					SUM(track_features.mode_major ::FLOAT) / COUNT(*) AS mode_major,
					
					MODE () WITHIN GROUP ( ORDER BY "time_signature" ) AS time_signature,
					SUM(track_features.time_signature_0 ::FLOAT) / COUNT(*) AS time_signature_0,
					SUM(track_features.time_signature_1 ::FLOAT) / COUNT(*) AS time_signature_1,
					SUM(track_features.time_signature_2 ::FLOAT) / COUNT(*) AS time_signature_2,
					SUM(track_features.time_signature_3 ::FLOAT) / COUNT(*) AS time_signature_3,
					SUM(track_features.time_signature_4 ::FLOAT) / COUNT(*) AS time_signature_4,
					SUM(track_features.time_signature_5 ::FLOAT) / COUNT(*) AS time_signature_5,
					SUM(track_features.time_signature_6 ::FLOAT) / COUNT(*) AS time_signature_6,
					SUM(track_features.time_signature_7 ::FLOAT) / COUNT(*) AS time_signature_7
					
		
FROM playlist
INNER JOIN track_features
ON playlist.track_uri = track_features.track_uri
GROUP BY playlist.pid
ORDER BY playlist.pid;

SELECT * FROM playlist_stat_mean_mode


-- **
SELECT * FROM track_recommendations

COPY track_recommendations FROM 'C:\Users\Christophe\OneDrive\Documents\Berkeley_Bootcamp\Section_23_ Project_4\Spotify\spotify_million_playlist_dataset\input_20_tracks.csv' WITH (FORMAT csv);


DROP VIEW IF EXISTS track_recommendation_features;
CREATE VIEW track_recommendation_features AS 
SELECT track_features.track_uri, track_features.danceability, track_features.energy, track_features.key, track_features.loudness, track_features.mode, track_features.speechiness,
       track_features.acousticness, track_features.instrumentalness, track_features.liveness, track_features.valence, track_features.tempo,
       track_features.duration_ms, track_features.time_signature, track_features.mode_minor, track_features.mode_major,
       track_features.key_none, track_features.key_0, track_features.key_1, track_features.key_2, track_features.key_3, track_features.key_4, track_features.key_5,
       track_features.key_6, track_features.key_7, track_features.key_8, track_features.key_9, track_features.key_10, track_features.key_11,
       track_features.time_signature_0, track_features.time_signature_1, track_features.time_signature_2,
       track_features.time_signature_3, track_features.time_signature_4, track_features.time_signature_5,
       track_features.time_signature_6, track_features.time_signature_7

FROM track_recommendations
INNER JOIN track_features
ON track_recommendations.track_uri = track_features.track_uri;


SELECT * FROM track_recommendation_features;



TRUNCATE track_recommendations;


-- New table to include stddev as features
DROP TABLE IF EXISTS playlist_stat_mean_std_mode_pct;
CREATE TABLE playlist_stat_mean_std_mode_pct AS 
SELECT playlist.pid, COUNT(*) AS tracks_found,
					AVG(track_features.danceability) AS danceability,
					STDDEV(track_features.danceability) AS danceability_std,
					AVG(track_features.energy) AS energy,
					STDDEV(track_features.energy) AS energy_std,
					AVG(track_features.loudness) AS loudness,
					STDDEV(track_features.loudness) AS loudness_std,
					AVG(track_features.speechiness) AS speechiness,
					STDDEV(track_features.speechiness) AS speechiness_std,
					AVG(track_features.acousticness) AS acousticness,
					STDDEV(track_features.acousticness) AS acousticness_std,
					AVG(track_features.instrumentalness) AS instrumentalness,
					STDDEV(track_features.instrumentalness) AS instrumentalness_std,
					AVG(track_features.liveness) AS liveness,
					STDDEV(track_features.liveness) AS liveness_std,
					AVG(track_features.valence) AS valence,
					STDDEV(track_features.valence) AS valence_std,
					AVG(track_features.tempo) AS tempo,
					STDDEV(track_features.tempo) AS tempo_std,
					AVG(track_features.duration_ms) AS duration_ms,
					STDDEV(track_features.duration_ms) AS duration_ms_std,
					
                    MODE () WITHIN GROUP ( ORDER BY "key" ) AS "key",
					SUM(track_features.key_none) / COUNT(*) AS key_none,
					SUM(track_features.key_0 ::FLOAT) / COUNT(*) AS key_0,
					SUM(track_features.key_1 ::FLOAT) / COUNT(*) AS key_1,
					SUM(track_features.key_2 ::FLOAT) / COUNT(*) AS key_2,
					SUM(track_features.key_3 ::FLOAT) / COUNT(*) AS key_3,
					SUM(track_features.key_4 ::FLOAT) / COUNT(*) AS key_4,
					SUM(track_features.key_5 ::FLOAT) / COUNT(*) AS key_5,
					SUM(track_features.key_6 ::FLOAT) / COUNT(*) AS key_6,
					SUM(track_features.key_7 ::FLOAT) / COUNT(*) AS key_7,
					SUM(track_features.key_8 ::FLOAT) / COUNT(*) AS key_8,
					SUM(track_features.key_9 ::FLOAT) / COUNT(*) AS key_9,
					SUM(track_features.key_10 ::FLOAT) / COUNT(*) AS key_10,
					SUM(track_features.key_11 ::FLOAT) / COUNT(*) AS key_11,

					MODE () WITHIN GROUP ( ORDER BY "mode" ) AS mode,
					SUM(track_features.mode_minor ::FLOAT) / COUNT(*) AS mode_minor,
					SUM(track_features.mode_major ::FLOAT) / COUNT(*) AS mode_major,
					
					MODE () WITHIN GROUP ( ORDER BY time_signature ) AS time_signature,
					SUM(track_features.time_signature_0 ::FLOAT) / COUNT(*) AS time_signature_0,
					SUM(track_features.time_signature_1 ::FLOAT) / COUNT(*) AS time_signature_1,
					SUM(track_features.time_signature_2 ::FLOAT) / COUNT(*) AS time_signature_2,
					SUM(track_features.time_signature_3 ::FLOAT) / COUNT(*) AS time_signature_3,
					SUM(track_features.time_signature_4 ::FLOAT) / COUNT(*) AS time_signature_4,
					SUM(track_features.time_signature_5 ::FLOAT) / COUNT(*) AS time_signature_5,
					SUM(track_features.time_signature_6 ::FLOAT) / COUNT(*) AS time_signature_6,
					SUM(track_features.time_signature_7 ::FLOAT) / COUNT(*) AS time_signature_7
					
				
		
FROM playlist
INNER JOIN track_features
ON playlist.track_uri = track_features.track_uri
GROUP BY playlist.pid
ORDER BY playlist.pid;