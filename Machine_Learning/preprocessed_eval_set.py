import pandas as pd
import numpy as np
import os

# 處理並儲存數據的函數
def process_and_save_reshaped_numpy(input_csv, output_dir):
    # 確保輸出目錄存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 初始化輸出檔案編號
    file_index = 1
        
    # 讀取每個 CSV 檔案
    data = pd.read_csv(input_csv)

    flag_range = 20
    count = 0
    # 處理 Start Flag 0 到 19
    for flag in range(0, flag_range):
        # 篩選出當前 flag 的資料
        flag_data = data[data['Start Flag'] == flag]

        # 如果該 flag 沒有資料，跳過
        if flag_data.empty:
            print(f"No data for Start Flag {flag} in {input_csv}")
            continue

        # 如果資料超過 30 點，裁剪到 30 點
        if len(flag_data) > 30:
            flag_data = flag_data.iloc[:30]
        
        # 如果資料不足 30 點，補 0
        if len(flag_data) < 30:
            padding_length = 30 - len(flag_data)
            padding = pd.DataFrame(
                np.zeros((padding_length, len(flag_data.columns))),
                columns=flag_data.columns
            )
            flag_data = pd.concat([flag_data, padding], ignore_index=True)

        # Reshape to (6, 30)
        chunk_data = np.array([
            flag_data['Accel X'].values,
            flag_data['Accel Y'].values,
            flag_data['Accel Z'].values,
            flag_data['Gyro X'].values,
            flag_data['Gyro Y'].values,
            flag_data['Gyro Z'].values
        ])
        
        # save as npy
        output_filename = os.path.join(output_dir, f"{file_index}.npy")
        np.save(output_filename, chunk_data)
        count+=1
        print(f"Saved: {output_filename}")
        file_index+=1

#-----------------------------------------------------------------------------------------
#Directory setting
input_csv= 'D:\\ESD_code\\AIOT\\IMU_data_process\\evluation_raw\\user2\\position\\high_abs.csv'  
output_directory = 'D:\\ESD_code\\AIOT\\IMU_data_process\\evaluation_set\\user2\\high\\situp'  

process_and_save_reshaped_numpy(input_csv, output_directory)
