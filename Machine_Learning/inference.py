# from model.LSTM import LSTMClassifier
from model.Attn_conv import Attn_conv

import torch
import json
import numpy as np



def infer(json_file):
    #Build model
    label_map = {'bicep': 0, 'abs': 1, 'chess': 2, 'leg': 3}
    #model = LSTMClassifier(n_class=4)
    #model.load_state_dict(torch.load("./model_state/LSTM.pth", weights_only=True))
    model = Attn_conv(n_class=4)
    model.load_state_dict(torch.load("./model_state/Attn_conv.pth", weights_only=True))
    model.eval()

    #Load imu data
    with open(json_file,"r") as file:
        data = json.load(file)
    channels = ["AccelX", "AccelY", "AccelZ", "GyroX", "GyroY", "GyroZ"]
    imu_data = np.array([data[channel] for channel in channels])

    #Process data
    len_data = imu_data.shape[1]
    window_size = 30
    overlap = 15
    step = window_size - overlap
    predictions = [0,0,0,0]
    

    for start in range(0,len_data,step):
        end = start + window_size
        if end > len_data:
            # Zero padding to last window
            window = np.pad(imu_data[:, start:], ((0, 0), (0, end - len_data)), mode='constant')
        else:
            window = imu_data[:, start:end]
        
        input_tensor = torch.tensor(window, dtype=torch.float32).unsqueeze(0)

        with torch.no_grad():
            output = model(input_tensor) 
            probabilities = torch.softmax(output, dim=-1).cpu().numpy()
            predicted_class = np.argmax(probabilities)
            #print(probabilities)
            if np.max(probabilities) > 0.70:    #Threshold
                predictions[predicted_class] += 1
    #取眾數
    max_count = max(predictions)
    predictions = [x if x == max_count else 0 for x in predictions]

    print(f"bicep: {predictions[0]} | abs: {predictions[1]} | chess: {predictions[2]} | legs: {predictions[3]}")

infer("./test_data.json")