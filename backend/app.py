from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import main
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
import pandas as pd

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3'}

# Store mp3 files in folder for possible later usage 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) 

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# API route to predict arousal/valence values of song
@app.route('/api/convert', methods=['POST'])
def conversion():
  if request.method == 'POST':
    title = request.form.get("title")
    artist = request.form.get("artist")
    if main.song_exists(title, artist):
      return jsonify({'error': 'Song already exists'}), 400
    if(title == '' or artist == ''):
      return jsonify({'error': 'No title or artist'}), 400
    if 'file' not in request.files:
      return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
      return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
      output_filepath = process_file(file)
      if os.path.exists(output_filepath):
        song_id = main.song_metadata(title, artist)
        db, waveform, sr = main.wav_to_spectro(output_filepath)
        pred = main.predictor(db, waveform, sr, song_id)
        valence = pred[0, 1].item()  # Extract valence value
        arousal = pred[0, 0].item()
        valence = max(0, min(valence, 1))  
        arousal = max(0, min(arousal, 1))     
        
        
        prediction_dict = {'arousal': arousal, 'valence': valence}
        return jsonify({'prediction': prediction_dict}), 200
      else:
        return jsonify({'error': 'Conversion failed'}), 500
    else:
      return jsonify({'error': 'Invalid file format'}), 400

# convert mp3 file into wav file
def process_file(file):
  basedir = os.path.abspath(os.path.dirname(__file__))
  file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], file.filename))
  input_filepath = os.path.join(basedir, app.config['UPLOAD_FOLDER'], file.filename)
  output_filename = os.path.splitext(file.filename)[0] + '.wav'
  output_filepath = os.path.join(basedir, app.config['UPLOAD_FOLDER'], output_filename)
  command = f'ffmpeg -i "{input_filepath}" "{output_filepath}"' # convert mp3 to wav
  subprocess.run(command, shell=True)
  return output_filepath
    
# API route to get all songs
@app.route('/api/home', methods=['GET'])
def home():
  songs_data = []
  results = main.song_data()
  for row in results:
            songs_data.append({
                'arousal': row[0],
                'valence': row[1],
                'title': row[2],
                'artist': row[3],
                'song_id': row[4]
            })
  return jsonify(songs_data)

# API route to recommend 5 songs close to chosen songs
@app.route('/api/recommend/<int:song_id>', methods=['GET'])
def reccomend(song_id):
  results = main.recommendation()
  results=preprocessing.scale(results)
  labels = main.labels()
  index_labels = [label[0] for label in labels]
  print("index label:", index_labels)
  df = pd.DataFrame(results)
  similarity = cosine_similarity(df) # Find similar songs
  sim_df = pd.DataFrame(similarity, index=index_labels, columns=index_labels)
  print("Results: ", results)
  print("song_id:", song_id)
  print("Labels:", labels)
  print("DataFrame index:", sim_df.index)
  series = sim_df[song_id].sort_values(ascending=False)
  series = series.drop(song_id)
  top_5 = series.head(5)
  song_ids = top_5.index.tolist()
  print("Top 5 similar songs:", song_ids)
  names = main.song_names(song_ids)
  song_data = []
  for i in range(len(names)):
    song_data.append({
      "title": names[i][0],
      "artist": names[i][1]
    })
  print(song_data)
  return jsonify(song_data)

# API route to insert playlist into database
@app.route('/api/playlists_insert', methods=['POST'])
def playlists_insert():
  data = request.json
  name = data.get("name")
  print(name)
  songs = data.get("songs", [])
  print(songs)
  song_ids = []
  for song in songs:
    song_id = song.get('song_id')
    song_ids.append(song_id)
  
  main.playlists_sql(name, song_ids)
  return jsonify({"message": "Playlist inserted successfully"})

# API route to retrieve all playlists
@app.route('/api/playlists', methods=['GET'])
def playlists():
  playlist_data=[]
  playlists = main.playlists_retrieve()
  for row in playlists:
            playlist_data.append({
                'name': row[0],
                'playlist_id': row[1],
                'song_ids': [row[2]]
                
            })
  return jsonify(playlist_data)

# API route to get all songs of a playlist
@app.route('/api/playlists_songs', methods=['GET'])
def playlists_songs():
  name = request.args.get('name')
  print(name)
  results = main.find_songs(name)
  print(results)
  songs_data = []
  for row in results:
            songs_data.append({
                'title': row[0],
                'artist': row[1],
                'song_id': row[2]
            })
  print(songs_data)
  return jsonify(songs_data)

# API route to delete chosen playlist
@app.route('/api/delete_playlist', methods=['DELETE'])
def delete_playlist():
  playlist_id = request.args.get('playlist_id')
  main.delete_play(playlist_id)
  return jsonify({'message': 'Playlist deleted successfully'}), 200

# API route to delete chosen song
@app.route('/api/delete_song', methods=['DELETE'])
def delete_song():
  song_id = request.args.get('song_id')
  main.delete_song(song_id)
  return jsonify({'message': 'Song deleted successfully'}), 200

if __name__== '__main__':
    app.run()
