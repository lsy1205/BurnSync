import torch
import torch.nn as nn

class LSTMClassifier(nn.Module):
    def __init__(self, n_class=4):
        super(LSTMClassifier, self).__init__()
        self.lstm = nn.LSTM(input_size=30, hidden_size=64, num_layers=2, batch_first=True)
        self.fc = nn.Linear(64, n_class)
    
    def forward(self, x):
        # Input shape: (batch_size, 6, 30)
        x, _ = self.lstm(x)  # LSTM 層，輸出形狀 (batch_size, 6, 64)
        x = x[:, -1, :]  # 選取最後一個時間步的輸出
        x = self.fc(x)  # 全連接層，輸出形狀 (batch_size, num_classes)
        return x
