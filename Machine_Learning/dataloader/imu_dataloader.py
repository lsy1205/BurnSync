import os
import numpy as np
import torch
import torch.utils.data
import torchaudio.transforms as T

class IMU(torch.utils.data.Dataset):
    def __init__(self,data_dir,mode):
        self.mode_dir = os.path.join(data_dir, mode)
        self.work_list = os.listdir(self.mode_dir)
        self.dataset = []
        self.label_map = {'bicep': 0, 'abs': 1, 'chess': 2, 'leg': 3}

        #Concat to [npy path, label]
        for work in self.work_list:
            data_list = os.listdir(os.path.join(self.mode_dir,work))
            for data in data_list:
                label_encoding  = [0] * len(self.label_map)
                label_encoding[self.label_map[work]] = 1
                self.dataset.append([os.path.join(self.mode_dir,work,data), np.array(label_encoding, dtype=np.float32)])

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        data = self.dataset[idx]
        #Label
        label = data[1]
        #Input
        input_data = np.load(data[0])
        input_tensor = torch.tensor(input_data, dtype=torch.float32)
        return input_tensor, label


def load_data(datapath, batch_size, num_workers):
    #Build dataset
    train_ds = IMU(datapath, "train")
    valid_ds = IMU(datapath, "valid")

    #Build dataloader
    trainset_loader = torch.utils.data.DataLoader(dataset=train_ds,
                                                  batch_size=batch_size,
                                                  pin_memory=True,
                                                  shuffle=True,
                                                  drop_last=True,
                                                  num_workers=num_workers)
    
    validset_loader = torch.utils.data.DataLoader(dataset=valid_ds,
                                                  batch_size=batch_size,
                                                  pin_memory=True,
                                                  shuffle=False,
                                                  drop_last=True,
                                                  num_workers=num_workers)
    
    return trainset_loader, validset_loader
