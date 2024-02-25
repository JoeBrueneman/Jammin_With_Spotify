-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "track_features" (
    "danceability" FLOAT   NOT NULL,
    "energy" FLOAT   NOT NULL,
    "key" INT   NOT NULL,
    "key_none" INT   NOT NULL,
    "key_0" INT   NOT NULL,
    "key_1" INT   NOT NULL,
    "key_2" INT   NOT NULL,
    "key_3" INT   NOT NULL,
    "key_4" INT   NOT NULL,
    "key_5" INT   NOT NULL,
    "key_6" INT   NOT NULL,
    "key_7" INT   NOT NULL,
    "key_8" INT   NOT NULL,
    "key_9" INT   NOT NULL,
    "key_10" INT   NOT NULL,
    "key_11" INT   NOT NULL,
    "loudness" FLOAT   NOT NULL,
    "mode" INT   NOT NULL,
    "mode_minor" INT   NOT NULL,
    "mode_major" INT   NOT NULL,
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

ALTER TABLE "track_features" ADD CONSTRAINT "fk_track_features_track_uri" FOREIGN KEY("track_uri")
REFERENCES "playlist" ("track_uri");

