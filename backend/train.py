import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
import numpy as np
import librosa
import pandas as pd
import glob
from model import MyModel
from sklearn.model_selection import train_test_split
from torch.nn.functional import pad
import sklearn
import warnings
warnings.filterwarnings('ignore')

model = torch.hub.load('harritaylor/torchvggish', 'vggish')
model.eval()


directory = '/Users/isiahketton/Downloads/mel_images'
if not os.path.exists(directory):
    os.makedirs(directory)
    
file_list = sorted(glob.glob('/Users/isiahketton/Downloads/PMEmo2019/chorus/wav/*.wav'))

# Path to csv file
csv_file = '/Users/isiahketton/Downloads/PMEmo2019/annotations/static_annotations.csv'
labels_df = pd.read_csv(csv_file)
mel_spec = []
emotion_values = []
features = []
for index, row in labels_df.iterrows(): # iterate through all rows
    music_id = int(row['musicId'])
    if os.path.isfile(os.path.join('/Users/isiahketton/Downloads/PMEmo2019/chorus/wav', f'{music_id}.wav')):
        wav_file = os.path.join('/Users/isiahketton/Downloads/PMEmo2019/chorus/wav', f'{music_id}.wav') # iterate through all wav files that actually have values in csv file
        # transform wav files into db mel spectrograms 
        waveform, sr = librosa.load(wav_file)
        spectrogram = librosa.feature.melspectrogram(y=waveform, sr=sr, hop_length=512, n_fft=2048)
        mel_abs = np.abs(spectrogram)
        db = librosa.power_to_db(mel_abs, ref=np.max)
        mel_spec.append(db) # append to array
        arousal_value = row.iloc[1] 
        valence_value = row.iloc[2]
        emotion_values.append((arousal_value, valence_value)) # append lables to array
        
# Longest Spectrogram
max_length = max(spec.shape[1] for spec in mel_spec)

# Pad or truncate each spectrogram to match the maximum length
padded_mel_spec = []
for spec in mel_spec:
    if spec.shape[1] < max_length:
        # Pad with zeros
        padded_spec = np.pad(spec, ((0, 0), (0, max_length - spec.shape[1])), mode='constant', constant_values=0)
    elif spec.shape[1] > max_length:
        # Truncate spectrogram
        padded_spec = spec[:, :max_length]
    else:
        # No need for padding or truncation
        padded_spec = spec
    padded_mel_spec.append(padded_spec)

# Convert the list of padded spectrograms to a numpy array
padded_mel_spec = np.array(padded_mel_spec)

# Split the data across training and validation sets
X_train, X_test, y_train, y_test = train_test_split(padded_mel_spec, emotion_values, test_size=0.2, random_state=42)
BATCH_SIZE = 50

torch_X_train = torch.unsqueeze(torch.tensor(X_train, dtype=torch.float32), 1)
torch_y_train = torch.tensor(y_train, dtype=torch.float32)

torch_X_test = torch.unsqueeze(torch.tensor(X_test, dtype=torch.float32), 1)
torch_y_test = torch.tensor(y_test, dtype=torch.float32)

train = torch.utils.data.TensorDataset(torch_X_train,torch_y_train)
test = torch.utils.data.TensorDataset(torch_X_test,torch_y_test)


train_loader = torch.utils.data.DataLoader(train, batch_size = BATCH_SIZE, shuffle = True)
test_loader = torch.utils.data.DataLoader(test, batch_size = BATCH_SIZE, shuffle = False)

    
device = 'cuda' if torch.cuda.is_available() else 'cpu' 
cost = nn.MSELoss()
lr = 0.00001
model = MyModel().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=lr)

# old train and test functions before early stopping implementation
'''
def train(dataloader, model, cost, optimizer):
    model.train()
    size = len(dataloader.dataset)
    for batch, (X,Y) in enumerate(dataloader):

        X, Y = X.to(device), Y.to(device)
        optimizer.zero_grad()

        pred = model(X)

        loss = cost(pred, Y)
        loss.backward()
        optimizer.step()
        if batch % 100 == 0:
            loss, curr = loss.item(), batch * len(X)
            print(f'loss: {loss:>7f}  [{curr:>5d}/{size:>5d}]')
def test(dataloader, model):
    size = len(dataloader.dataset)
    model.eval()
    test_loss, correct = 0, 0

    with torch.no_grad():
        for batch, (X, Y) in enumerate(dataloader):
            X, Y = X.to(device), Y.to(device)
            pred = model(X)
            test_loss += cost(pred, Y).item()

            correct += (pred.argmax(1)==Y.argmax(1)).sum().item()

    test_loss /= size
    correct /= size

    print(f'\nTest Error:\nacc: {(100*correct):>0.1f}%, avg loss: {test_loss:>8f}\n')
    '''
    
epochs = 30

#for t in range(epochs):
   # print(f'Epoch {t+1}\n-------------------------------')
   # train(train_loader, model, cost, optimizer)
   # test(test_loader, model)
#print('Done!')

# training with early stopping implemention
def train_with_early_stopping(train_loader, val_loader, model, cost, optimizer, patience):
    best_val_loss = float('inf')
    counter = 0
    
    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        correct_train = 0
        
        for (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = cost(output, target)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * data.size(0)
            correct_train += (output.argmax(1) == target.argmax(1)).sum().item()
        
        train_loss /= len(train_loader.dataset)
        train_accuracy = correct_train / len(train_loader.dataset)
        
        # Validate the model
        model.eval()
        val_loss = 0.0
        correct_val = 0
        
        with torch.no_grad():
            for data, target in val_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                loss = cost(output, target)
                val_loss += loss.item() * data.size(0)
                correct_val += (output.argmax(1) == target.argmax(1)).sum().item()
        
        val_loss /= len(val_loader.dataset)
        val_accuracy = correct_val / len(val_loader.dataset)
        
        print(f'Epoch {epoch+1}/{epochs}, Train Loss: {train_loss}, Train Accuracy: {train_accuracy}, Val Loss: {val_loss}, Val Accuracy: {val_accuracy}')
        
        # Check for early stopping
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            counter = 0
            # Save the best model
            torch.save(model.state_dict(), 'best_model.pth')
        else:
            counter += 1
            if counter >= patience:
                print(f'Validation loss did not improve for {patience} epochs. Early stopping...')
                break
            
            
train_with_early_stopping(train_loader, test_loader, model, cost, optimizer, patience=5)
    



