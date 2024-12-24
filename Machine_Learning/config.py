import argparse

#Config for training model
def get_config():
    parser = argparse.ArgumentParser()

    parser.add_argument("--epochs", type=int, default=100, help="number of epochs")
    parser.add_argument("--batch_size", type=int, default=8, help="number per batch")
    parser.add_argument("--data_path", type=str, default="D:\ESD_code\AIOT\IMU_data_process\data_split")
    parser.add_argument("--model", type=str, default="CRNN", help="model name")
    parser.add_argument("--model_save_path", type=str, default="./model_state/Attn_conv.pth")
    parser.add_argument("--curve_save_path", type=str, default="./curve/Attn_conv")
    parser.add_argument("--init_lr", type=float, default=3e-3)
    parser.add_argument('--early_stop', type=int, default=10)
    parser.add_argument("--l2_lambda", type=float, default=1e-2)

    args = parser.parse_args()
    return args