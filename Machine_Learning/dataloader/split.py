import os
import shutil
import argparse
import random

def split(args):
    # 获取原始路径下的所有类别文件夹
    pos_list = os.listdir(args.org_path)

    for pos in pos_list:
        pos_folder = os.path.join(args.org_path, pos, "npy")
        pos_files = os.listdir(pos_folder)

        # 打乱文件顺序
        random.shuffle(pos_files)

        # 数据集分割比例
        num_data = len(pos_files)
        train_size = int(num_data * 0.7)
        valid_size = int(num_data * 0.15)

        # 分割为 train, valid, test
        train_files = pos_files[:train_size]
        valid_files = pos_files[train_size:train_size + valid_size]
        test_files = pos_files[train_size + valid_size:]

        # 创建新的目录
        new_train_folder = os.path.join(args.new_path, "train", pos)
        new_valid_folder = os.path.join(args.new_path, "valid", pos)
        new_test_folder = os.path.join(args.new_path, "test", pos)

        os.makedirs(new_train_folder, exist_ok=True)
        os.makedirs(new_valid_folder, exist_ok=True)
        os.makedirs(new_test_folder, exist_ok=True)

        # 复制文件到对应的目录
        for file in train_files:
            shutil.copy(os.path.join(pos_folder, file), os.path.join(new_train_folder, file))

        for file in valid_files:
            shutil.copy(os.path.join(pos_folder, file), os.path.join(new_valid_folder, file))

        for file in test_files:
            shutil.copy(os.path.join(pos_folder, file), os.path.join(new_test_folder, file))


#----------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--org_path", type=str, default="D:\\ESD_code\\AIOT\\IMU_data_process\\dataset")
    parser.add_argument("--new_path", type=str, default="D:\\ESD_code\\AIOT\\IMU_data_process\\data_split")
    args = parser.parse_args()

    split(args)
