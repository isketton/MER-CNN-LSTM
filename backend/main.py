import torch
import librosa
import numpy as np
from model import MyModel
import sklearn
import mysql.connector
import os
import sklearn 
from sklearn.preprocessing import scale, MinMaxScaler
import logging 

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 

handler = logging.StreamHandler()  # Print to console


formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# MySQL connection, i did not host on a public server so must have own sql server active, input details
dbconfig = {
    "host":"127.0.0.1",
    "port":"3306",
    "user":"root",
    "password":"password1",
    "database":"audio_features",
}
try:  
  con = mysql.connector.connect(pool_name = "mypool", pool_size = 30, **dbconfig)
  logger.info("Connected to the database")
except mysql.connector.Error as err:
  logger.error(f"Error connecting to the database: {err}")
  raise

# convert uploaded wav file into spectrogram and then tensor for model input
def wav_to_spectro(wav_file):
  waveform, sr = librosa.load(wav_file)
  spectrogram = librosa.feature.melspectrogram(y=waveform, sr=sr, hop_length=512, n_fft=2048)
  mel_abs = np.abs(spectrogram)
  db = librosa.power_to_db(mel_abs, ref=np.max)
  db_tensor = torch.unsqueeze(torch.tensor(db, dtype=torch.float32), 0)
  return db_tensor, waveform, sr

# Load model and evaluate spectrogram for arousal/valence prediction
def predictor(X, waveform, sr, song_id):
  device = 'cuda' if torch.cuda.is_available() else 'cpu'
  model = MyModel()
  model.load_state_dict(torch.load('/Users/isiahketton/Desktop/CS 152 Proj/backend/best_model3.pth', map_location=torch.device('cpu')))
  model.to(device)
  X = X.unsqueeze(0).to(device)
  model.eval()
  with torch.no_grad():
    output = model(X)
  features(waveform, sr, output, song_id) # extract spectral features from uploaded songs
  return output
  
# Extract spectral features from uploaded songs
def features(waveform, sr, output, song_id):
  try:
    cursor = con.cursor()
    valence = output[0, 1].item()
    arousal = output[0, 0].item()
    chroma_stft = librosa.feature.chroma_stft(y=waveform, sr=sr)
    chroma_stft_mean = chroma_stft.mean()
    chroma_stft_var = chroma_stft.var()
    chroma_stft_mean = float(chroma_stft_mean)
    chroma_stft_var = float(chroma_stft_var)
          
    rms = librosa.feature.rms(y=waveform)
    rms_mean = rms.mean()
    rms_var = rms.var()
    rms_mean = float(rms_mean)
    rms_var = float(rms_var)
          
    spectral_centroids = librosa.feature.spectral_centroid(y=waveform, sr=sr)
    spectral_centroids_mean = spectral_centroids.mean()
    spectral_centroids_var = spectral_centroids.var()
    spectral_centroids_mean = float(spectral_centroids_mean)
    spectral_centroids_var = float(spectral_centroids_var)

    spectral_bandwidths = librosa.feature.spectral_bandwidth(y=waveform, sr=sr)
    spectral_bandwidths_mean = spectral_bandwidths.mean()
    spectral_bandwidths_var = spectral_bandwidths.var()
    spectral_bandwidths_mean = float(spectral_bandwidths_mean)
    spectral_bandwidths_var = float(spectral_bandwidths_var)
          
    spectral_rolloff = librosa.feature.spectral_rolloff(y=waveform, sr=sr)
    spectral_rolloff_mean = spectral_rolloff.mean()
    spectral_rolloff_var= spectral_rolloff.var()
    spectral_rolloff_mean = float(spectral_rolloff_mean)
    spectral_rolloff_var = float(spectral_rolloff_var)
          
    zero_crossing_rates = librosa.feature.zero_crossing_rate(y=waveform)
    zero_crossing_rates_mean = zero_crossing_rates.mean()
    zero_crossing_rates_var = zero_crossing_rates.var()
    zero_crossing_rates_mean = float(zero_crossing_rates_mean)
    zero_crossing_rates_var = float(zero_crossing_rates_var)
          
    chroma_cens = librosa.feature.chroma_cens(y=waveform, sr=sr)
    harmony_mean = chroma_cens.mean()
    harmony_var = chroma_cens.var()
    harmony_mean = float(harmony_mean)
    harmony_var = float(harmony_var)
          
    S = np.abs(librosa.stft(y=waveform))
    frequencies = librosa.core.fft_frequencies(sr=sr)
    perceptr = librosa.perceptual_weighting(S**2, frequencies)
    perceptr_mean = perceptr.mean()
    perceptr_var = perceptr.var()
    perceptr_mean = float(perceptr_mean)
    perceptr_var = float(perceptr_var)
          
    tempo = librosa.beat.tempo(y=waveform, sr=sr)
    tempo_mean = float(tempo.mean())
          
    mfccs = librosa.feature.mfcc(y=waveform, sr=sr, n_mfcc=20)
          # Apply Feature Scaling
    mfccs = scale(mfccs, axis=1)
    means = [mfccs[:, i].mean() for i in range(0, 20)]
    vars_tmp = [mfccs[:, i].var() for i in range(0, 20)]
    
    means = [float(m) for m in means]
    vars_tmp = [float(v) for v in vars_tmp]
    
    mfccs1_mean, mfccs2_mean, mfccs3_mean, mfccs4_mean, mfccs5_mean = means[:5]
    mfccs6_mean, mfccs7_mean, mfccs8_mean, mfccs9_mean, mfccs10_mean = means[5:10]
    mfccs11_mean, mfccs12_mean, mfccs13_mean, mfccs14_mean, mfccs15_mean = means[10:15]
    mfccs16_mean, mfccs17_mean, mfccs18_mean, mfccs19_mean, mfccs20_mean = means[15:20]
    
    mfccs1_var, mfccs2_var, mfccs3_var, mfccs4_var, mfccs5_var = vars_tmp[:5]
    mfccs6_var, mfccs7_var, mfccs8_var, mfccs9_var, mfccs10_var = vars_tmp[5:10]
    mfccs11_var, mfccs12_var, mfccs13_var, mfccs14_var, mfccs15_var = vars_tmp[10:15]
    mfccs16_var, mfccs17_var, mfccs18_var, mfccs19_var, mfccs20_var = vars_tmp[15:20]

  #mfccs_mean_1_20 = mfccs[:, :20].mean(axis=0)
  #mfccs_var_1_20 = mfccs[:, :20].var(axis=0)
  
  
  #mfccs_mean_1_20 = float(mfccs_mean_1_20)
  #mfccs_var_1_20 = float(mfccs_var_1_20)
    insert_query = """
      INSERT INTO audio_data 
      (song_id, chroma_stft_mean, chroma_stft_var, 
      rms_mean, rms_var, 
      spectral_centroids_mean, spectral_centroids_var, 
      spectral_bandwidths_mean, spectral_bandwidths_var, 
      spectral_rolloff_mean, spectral_rolloff_var, 
      zero_crossing_rates_mean, zero_crossing_rates_var, 
      harmony_mean, harmony_var, 
      perceptr_mean, perceptr_var, 
      tempo_mean, 
      mfcc1_mean, mfcc2_mean, mfcc3_mean, mfcc4_mean, mfcc5_mean,
                                mfcc6_mean, mfcc7_mean, mfcc8_mean, mfcc9_mean, mfcc10_mean,
                                mfcc11_mean, mfcc12_mean, mfcc13_mean, mfcc14_mean, mfcc15_mean,
                                mfcc16_mean, mfcc17_mean, mfcc18_mean, mfcc19_mean, mfcc20_mean, 
      mfcc1_var, mfcc2_var, mfcc3_var, mfcc4_var, mfcc5_var,
                                mfcc6_var, mfcc7_var, mfcc8_var, mfcc9_var, mfcc10_var,
                                mfcc11_var, mfcc12_var, mfcc13_var, mfcc14_var, mfcc15_var,
                                mfcc16_var, mfcc17_var, mfcc18_var, mfcc19_var, mfcc20_var, 
      arousal, valence)
      VALUES 
      (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
      song_id, chroma_stft_mean, chroma_stft_var, 
      rms_mean, rms_var, 
      spectral_centroids_mean, spectral_centroids_var, 
      spectral_bandwidths_mean, spectral_bandwidths_var, 
      spectral_rolloff_mean, spectral_rolloff_var, 
      zero_crossing_rates_mean, zero_crossing_rates_var, 
      harmony_mean, harmony_var, 
      perceptr_mean, perceptr_var, 
      tempo_mean, 
      mfccs1_mean, mfccs2_mean, mfccs3_mean, mfccs4_mean, mfccs5_mean,
                mfccs6_mean, mfccs7_mean, mfccs8_mean, mfccs9_mean, mfccs10_mean,
                mfccs11_mean, mfccs12_mean, mfccs13_mean, mfccs14_mean, mfccs15_mean,
                mfccs16_mean, mfccs17_mean, mfccs18_mean, mfccs19_mean, mfccs20_mean, 
      mfccs1_var, mfccs2_var, mfccs3_var, mfccs4_var, mfccs5_var,
                 mfccs6_var, mfccs7_var, mfccs8_var, mfccs9_var, mfccs10_var,
                 mfccs11_var, mfccs12_var, mfccs13_var, mfccs14_var, mfccs15_var,
                 mfccs16_var, mfccs17_var, mfccs18_var, mfccs19_var, mfccs20_var,
      arousal, valence
    ))
    cursor.close()
    con.commit()
    logger.info("Features inserted successfully into the database")
  except mysql.connector.Error as error:
        print(f"Error inserting features into the database: {error}")
        con.rollback()
        raise
  finally:
        cursor.close()
    

# SQL query to input song metadata
def song_metadata(title, artist):
  cursor = con.cursor()
  try:
    insert_query = """
      INSERT INTO song_metadata (title, artist)
      VALUES (%s, %s)
    """ 
    cursor.execute(insert_query, (title, artist))  
    con.commit()
    return cursor.lastrowid
  except mysql.connector.Error as error:
        print(f"Error inserting song metadata: {error}")
      
# SQL query to tell whether a song exists within the database or not  
def song_exists(title, artist):
  cursor = con.cursor()
  sql = """
    SELECT COUNT(*)
    FROM song_metadata
    WHERE artist = %s AND title = %s
  """
  cursor.execute(sql, (artist, title))
  count_result = cursor.fetchone()
  cursor.close()
  if count_result is not None and count_result[0] > 0:
    return True
  else:
    return False

# SQL query to get chosen song arousal, valance, title, artist, and song id
def song_data():
  cursor = con.cursor()
  sql = """
    SELECT f.arousal, f.valence, s.title, s.artist, s.song_id 
    FROM song_metadata AS s
    JOIN audio_data AS f ON f.song_id = s.song_id
  """
  cursor.execute(sql)
  results = cursor.fetchall()
  cursor.close()
  return results

# SQL query to retrieve spectral features of chosen song from database for recommendations
def recommendation():
  cursor = con.cursor()
  sql = """
  SELECT chroma_stft_mean, chroma_stft_var, 
      rms_mean, rms_var, 
      spectral_centroids_mean, spectral_centroids_var, 
      spectral_bandwidths_mean, spectral_bandwidths_var, 
      spectral_rolloff_mean, spectral_rolloff_var, 
      zero_crossing_rates_mean, zero_crossing_rates_var, 
      harmony_mean, harmony_var, 
      perceptr_mean, perceptr_var, 
      tempo_mean, 
      mfcc1_mean, mfcc2_mean, mfcc3_mean, mfcc4_mean, mfcc5_mean,
                                mfcc6_mean, mfcc7_mean, mfcc8_mean, mfcc9_mean, mfcc10_mean,
                                mfcc11_mean, mfcc12_mean, mfcc13_mean, mfcc14_mean, mfcc15_mean,
                                mfcc16_mean, mfcc17_mean, mfcc18_mean, mfcc19_mean, mfcc20_mean, 
      mfcc1_var, mfcc2_var, mfcc3_var, mfcc4_var, mfcc5_var,
                                mfcc6_var, mfcc7_var, mfcc8_var, mfcc9_var, mfcc10_var,
                                mfcc11_var, mfcc12_var, mfcc13_var, mfcc14_var, mfcc15_var,
                                mfcc16_var, mfcc17_var, mfcc18_var, mfcc19_var, mfcc20_var, 
      arousal, valence
  FROM audio_data
  """
  cursor.execute(sql)
  results = cursor.fetchall()
  cursor.close()
  return results

# SQL query to get song id 
def labels():
  cursor = con.cursor()
  sql = """
  SELECT song_id 
  FROM audio_data
  """
  cursor.execute(sql)
  results = cursor.fetchall()
  cursor.close()
  return results

# SQL query to get song data from song ids
def song_names(song_ids):
  cursor = con.cursor()
  sql = """
  SELECT title, artist
  FROM song_metadata
  WHERE song_id IN (%s, %s, %s, %s, %s)
  """
  cursor.execute(sql, song_ids)
  results = cursor.fetchall()
  cursor.close()
  return results

# SQL queries to insert songs into playlists
def playlists_sql(name, song_ids):
  print(name)
  cursor = con.cursor()
  sql = """
  INSERT INTO playlists (playlist_name)
  VALUES (%s)
  """
  cursor.execute(sql, (name,))  
  con.commit()
  playlist_id = cursor.lastrowid 
  for song_id in song_ids:
    sql3 = """
    INSERT INTO playlists_songs (playlist_id, song_id)
    VALUES (%s, %s)
    """
    cursor.execute(sql3, (playlist_id, song_id))
  con.commit()
  cursor.close()
  
# SQL query to retrieve playlists
def playlists_retrieve():
  cursor = con.cursor()
  sql = """
  SELECT p.playlist_name, p.playlist_id, GROUP_CONCAT(ps.song_id) AS song_ids 
  FROM playlists p
  JOIN playlists_songs ps ON p.playlist_id = ps.playlist_id
  GROUP BY p.playlist_id
  """
  cursor.execute(sql)
  results = cursor.fetchall()
  cursor.close()
  return results

# SQL query to find songs from playlist
def find_songs(name):
  cursor = con.cursor()
  sql = """
  SELECT s.title, s.artist, s.song_id
  FROM playlists p
  JOIN playlists_songs ps ON p.playlist_id = ps.playlist_id
  JOIN song_metadata s ON ps.song_id = s.song_id
  WHERE p.playlist_name = %s
  """
  cursor.execute(sql, (name,))
  results = cursor.fetchall()
  cursor.close()
  return results

# SQL query to delete playlist
def delete_play(playlist_id):
  cursor = con.cursor()
  cursor.execute("DELETE FROM playlists_songs WHERE playlist_id = %s", (playlist_id,))
  cursor.execute("DELETE FROM playlists WHERE playlist_id = %s", (playlist_id,))
  con.commit()
  cursor.close()

# SQL query to delete song
def delete_song(song_id):
  logger.debug("Connecting to database")
  cursor = con.cursor()
  logger.debug("Deleting song features")
  cursor.execute("DELETE FROM audio_data WHERE song_id = %s", (song_id,))
  cursor.execute("DELETE FROM playlists_songs WHERE song_id = %s", (song_id,))
  cursor.execute("DELETE FROM song_metadata WHERE song_id = %s", (song_id,))
  logger.debug("Committing changes")
  con.commit()
  cursor.close()