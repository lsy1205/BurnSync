#from model.LSTM import LSTMClassifier
from model.Attn_conv import Attn_conv

import os
import torch
import numpy as np
import argparse
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from tqdm import tqdm 


def test(args):
    #Build model
    device = torch.device("cpu")
    #model = LSTMClassifier(n_class=4).to(device)
    model = Attn_conv(n_class=4).to(device)
    model.load_state_dict(torch.load(args.model_path, weights_only=True))
    model.eval()

    label_map = {'dumbbell': 0, 'situp': 1, 'pushup': 2, 'squat': 3}
    class_names = list(label_map.keys())
    work_list = os.listdir(args.test_path)
    num_data = 0
    correct = 0
    y_true = []
    y_predict = []
    for work in work_list:
        work_folder = os.path.join(args.test_path,work)
        data_list = os.listdir(work_folder)
        for data in tqdm(data_list):
            num_data += 1
            data_path = os.path.join(work_folder,data)
            input_data = np.load(data_path)
            input_tensor = torch.tensor(input_data, dtype=torch.float32).unsqueeze(0).to(device)
            with torch.no_grad():
                output = model(input_tensor)
                probabilities = torch.softmax(output, dim=-1).cpu().numpy()
            prediction = np.argmax(probabilities)
            
            label = label_map[work]
            y_true.append(label)
            y_predict.append(prediction)
            if prediction == label_map[work]:
                 correct += 1
            # else:
            #     print(probabilities, label_map[work])
    print(f"Final song acc: {correct/num_data}")
    # Confusion Matrix
    conf_matrix = confusion_matrix(y_true, y_predict)

    # Plotting the Confusion Matrix
    disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=class_names)
    disp.plot(cmap=plt.cm.Blues, values_format='d')
    # 保存混淆矩阵图像
    plt.title("Confusion Matrix")
    plt.savefig(args.plot_path, dpi=300, bbox_inches='tight')
    plt.close()

#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_path", type=str, default="D:\\ESD_code\\AIOT\\IMU_data_process\\evaluation_set\\user2\\right")
    parser.add_argument("--model_path", type=str, default="D:\\ESD_code\\AIOT\\IMU_data_process\\Machine_Learning\\model_state\\Attn_conv.pth")
    parser.add_argument("--plot_path", type=str, default="D:\\ESD_code\\AIOT\\IMU_data_process\\Machine_Learning\\plot\\user2_right.png")
    args = parser.parse_args()

    test(args)