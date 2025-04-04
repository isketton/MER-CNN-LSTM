# Music Emotion Recognition: CNN-LSTM

A full-stack ML system that classifies emotions from audio tracks using a CNN-LSTM deep learning model, with a React frontend and database storage.

## Features

- AI Model: Hybrid CNN-LSTM model in PyTorch for emotion classification (e.g., happy, sad, angry)

- Frontend: Interactive React dashboard for uploading songs and visualizing predictions

- Backend: Python (Flask) serving model predictions via REST API

- Database: Stores user uploads, predictions, and metadata (MySQL)

- Dataset: Trained on PMEmo2019

## Prerequisites
- Python 3.9+
- Docker

## Installation
1. git clone https://github.com/isketton/MER-CNN-LSTM.git

2. Start own MySQL server

3. Open vs code

4. Go to audio_features.sql, run for own database

5. once you're in the CS 152 Proj folder, in the terminal input:

```jsx
npm i
```

5. Go to the backend folder

```jsx
cd backend
```

6. once the directory is set to backend to start the flask server, in the terminal input:

```jsx
flask run
```

7. Open a second terminal and go to the frontend-app folder

```jsx
cd UI
```

8. once the directory is set to UI to start the React webpage, in the terminal input:

```jsx
npm start
```
9. For the mp3 files go to PMEmo2019 and download dataset

```jsx
https://github.com/HuiZhangDB/PMEmo
```


