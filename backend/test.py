import csv
import os
from math import ceil
import pandas as pd
import shutil
# This file is for culling overrepresented classes within the dataset

# Define paths,  replace with your actual WAV folder path
labels_df = pd.read_csv("/Users/isiahketton/Downloads/PMEmo2019/annotations/static_annotations.csv")  # Replace with your actual CSV file path
quarters_folder = '/Users/isiahketton/Downloads/PMEmo2019/chorus/wav'  # Folder to store split WAV files (create if needed)

# Create dictionaries for music data and quarter folders
music_data = {}
quarters = {
    "q3": os.path.join(quarters_folder, "q3"),
    "q4": os.path.join(quarters_folder, "q4"),
    "q1": os.path.join(quarters_folder, "q1"),
    "q2": os.path.join(quarters_folder, "q2"),
}

# Create quarter folders if they don't exist
for folder in quarters.values():
    os.makedirs(folder, exist_ok=True)  # Create folders if they don't exist

valence_threshold = 0.5
arousal_threshold = 0.5
# Read CSV data
for index, row in labels_df.iterrows():
    music_id = int(row['musicId'])
    arousal = row['Arousal(mean)']
    valence = row['Valence(mean)']
    if valence <= valence_threshold:
        if arousal <= arousal_threshold:
            quarter = 'q3'
        else:
            quarter = 'q1'
    else:
        if arousal <= arousal_threshold:
            quarter = 'q4'
        else:
            quarter = 'q2'

    # Define source and destination paths
    src_wav_file = f'/Users/isiahketton/Downloads/PMEmo2019/chorus/wav/{music_id}.wav'
    dest_dir = quarters[quarter]

    # Copy or move the WAV file to the appropriate quarter directory
    shutil.copy(src_wav_file, dest_dir)