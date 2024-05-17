import torch
import torch.nn as nn
import os
import pandas as pd

class MyModel(nn.Module):
    def __init__(self, hidden_size = 128):
        super(MyModel, self).__init__()
        # conv layer one/ Feature extraction
        # conv2d: 1: # of input channel(spectrogram), 
        # 64: # of output channels depth of feature map
        # kernel size: convolutional kernel, convolve over 3x3 window over input
        # padding: one pixel of padding around input
        # batchNorm2d: Applies Batch Normalization over a 4D input (a mini-batch of 2D inputs with additional channel dimension)
            # helps training process(faster)
        # ReLU: rectified linear unit(speed up training)
        # MaxPool2d; max pooling layer reduces spatial dimension of input feature map within each 2x2 window
        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size = (3, 3), padding = 1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, padding = 1)
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(64, 64, kernel_size=(3, 3), padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, padding=1)
        )

        self.conv3 = nn.Sequential(
            nn.Conv2d(64, 64, kernel_size=(3, 3), padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, padding=1)
        )
 
        self.conv4 = nn.Sequential(
            nn.Conv2d(64, 256, kernel_size=(3, 3), padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(2, padding=1)
        )
        self.hidden_size = hidden_size
        self.dropout = nn.Dropout(0.5)
        # Long Short-Term Memory (LSTM) is a type of Recurrent Neural Network (RNN) capable of learning and remembering information over time.
        self.lstm1 = nn.LSTM(256, self.hidden_size, 2, batch_first = True)
        # (Fully Connected) Linear transformation with 128 input features, 2 output 
        self.dense = nn.Linear(128, 2)
        
        
    def forward(self, x):
        out = self.conv1(x)
        out = self.conv2(out)
        out = self.conv3(out)
        out = self.conv4(out)

        # Applies droput regularization(Helps prevent overfitting)
        out = self.dropout(out)
       
        # For resizes out to have fixed 1x1 spatial dimension regardless of input size
        out = torch.nn.functional.adaptive_avg_pool2d(out, (1, out.size()[3]))
        # Reshapes into 3D tensor, 2nd dimension flattened
        out = out.view(out.size()[0], out.size()[1] * out.size()[2], -1)
        # Swaps 2nd and 3rd dimensions, tensor memory contiguous
        out = out.transpose(1, 2).contiguous()
        out, _ = self.lstm1(out)
        out = out.mean(dim=1)
        out = self.dense(out)
        #out = self.dense(out[:, -1, :])
            
        return out