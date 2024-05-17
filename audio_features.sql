CREATE DATABASE IF NOT EXISTS audio_features;

USE audio_features;


CREATE TABLE song_metadata (
  song_id INT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(255),
  artist VARCHAR(255)
);

USE audio_features;
CREATE TABLE audio_data (
  audio_id INT PRIMARY KEY AUTO_INCREMENT,
  song_id INT,  
  chroma_stft_mean FLOAT, 
  chroma_stft_var FLOAT,              -- Mean of chroma features
  rms_mean FLOAT,                       -- Mean of root mean square
  rms_var FLOAT,                        -- Variance of root mean square
  spectral_centroids_mean FLOAT,        -- Mean of spectral centroids
  spectral_centroids_var FLOAT,         -- Variance of spectral centroids
  spectral_bandwidths_mean FLOAT,       -- Mean of spectral bandwidths
  spectral_bandwidths_var FLOAT,        -- Variance of spectral bandwidths
  spectral_rolloff_mean FLOAT,          -- Mean of spectral rolloff
  spectral_rolloff_var FLOAT,           -- Variance of spectral rolloff
  zero_crossing_rates_mean FLOAT,       -- Mean of zero crossing rates
  zero_crossing_rates_var FLOAT,        -- Variance of zero crossing rates
  harmony_mean FLOAT,                   -- Mean of chroma features (chroma_cens)
  harmony_var FLOAT,                    -- Variance of chroma features (chroma_cens)
  perceptr_mean FLOAT,                   -- Mean of perceptual weighting
  perceptr_var FLOAT,                    -- Variance of perceptual weighting
  tempo_mean FLOAT,                     -- Mean tempo
  mfcc1_mean FLOAT NOT NULL,
  mfcc2_mean FLOAT NOT NULL,
  mfcc3_mean FLOAT NOT NULL,
  mfcc4_mean FLOAT NOT NULL,
  mfcc5_mean FLOAT NOT NULL,
  mfcc6_mean FLOAT NOT NULL,
  mfcc7_mean FLOAT NOT NULL,
  mfcc8_mean FLOAT NOT NULL,
  mfcc9_mean FLOAT NOT NULL,
  mfcc10_mean FLOAT NOT NULL,
  mfcc11_mean FLOAT NOT NULL,
  mfcc12_mean FLOAT NOT NULL,
  mfcc13_mean FLOAT NOT NULL,
  mfcc14_mean FLOAT NOT NULL,
  mfcc15_mean FLOAT NOT NULL,
  mfcc16_mean FLOAT NOT NULL,
  mfcc17_mean FLOAT NOT NULL,
  mfcc18_mean FLOAT NOT NULL,
  mfcc19_mean FLOAT NOT NULL,
  mfcc20_mean FLOAT NOT NULL,                    -- Mean of MFCCs (after scaling)
  mfcc1_var FLOAT NOT NULL,
  mfcc2_var FLOAT NOT NULL,
  mfcc3_var FLOAT NOT NULL,
  mfcc4_var FLOAT NOT NULL,
  mfcc5_var FLOAT NOT NULL,
  mfcc6_var FLOAT NOT NULL,
  mfcc7_var FLOAT NOT NULL,
  mfcc8_var FLOAT NOT NULL,
  mfcc9_var FLOAT NOT NULL,
  mfcc10_var FLOAT NOT NULL,
  mfcc11_var FLOAT NOT NULL,
  mfcc12_var FLOAT NOT NULL,
  mfcc13_var FLOAT NOT NULL,
  mfcc14_var FLOAT NOT NULL,
  mfcc15_var FLOAT NOT NULL,
  mfcc16_var FLOAT NOT NULL,
  mfcc17_var FLOAT NOT NULL,
  mfcc18_var FLOAT NOT NULL,
  mfcc19_var FLOAT NOT NULL,
  mfcc20_var FLOAT NOT NULL,
  arousal FLOAT,
  valence FLOAT,  
  FOREIGN KEY (song_id) REFERENCES song_metadata(song_id)                  
);


USE audio_features;
CREATE TABLE playlists (
  playlist_id INT PRIMARY KEY AUTO_INCREMENT,
  playlist_name VARCHAR(255)
);

USE audio_features;
CREATE TABLE playlists_songs (
  playlist_id INT,
  song_id INT,
  FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id),
  FOREIGN KEY (song_id) REFERENCES song_metadata(song_id),
  PRIMARY KEY (playlist_id, song_id)
);