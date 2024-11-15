import csv
import pandas as pd
import numpy as np
import os

##################################
# Add class line to the csv file #
##################################

def add_class(csv_file, fault_type, start_time, end_time):
    rows = []

    with open(csv_file, mode='r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Skip header
        header.append('class')

        for row in csv_reader:
            value = float(row[0])  # Assuming age is in the second column
            new_value = fault_type if start_time < value < end_time else 0
            row.append(new_value)  # Append the new value to the row
            rows.append(row)

    # Write the modified data back to the CSV file
    with open(csv_file, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)  # Write the updated header
        csv_writer.writerows(rows)    # Write the updated rows

################
# Making Noise #
################

def define_DATA_NAMES():
    DATA_NAMES = []

    # for gen_num in range(1,11):
    #     for phase_num in range(1,4):
    #         V_NAME = 'G'+str(gen_num)+'_V:'+str(phase_num)
    #         I_NAME = 'G'+str(gen_num)+'_I:'+str(phase_num)
    #         DATA_NAMES.append(V_NAME)
    #         DATA_NAMES.append(I_NAME)
    
    for gen_num in range(1,40):
        for phase_num in range(1,4):
            V_NAME = 'B'+str(gen_num)+'_V:'+str(phase_num)
            # I_NAME = 'T'+str(gen_num)+'_I:'+str(phase_num)
            DATA_NAMES.append(V_NAME)
            # DATA_NAMES.append(I_NAME)

    for gen_num in range(1,40):
        Vrms_NAME = 'B'+str(gen_num)+'_Vrms'
        angle_NAME = 'B'+str(gen_num)+'_angle'
        DATA_NAMES.append(Vrms_NAME)
        DATA_NAMES.append(angle_NAME)

    return DATA_NAMES

PERCENT = 5 #[%]
NOISE_STD_DEVIATION = PERCENT/100
DATA_NAMES = define_DATA_NAMES()

train_name = "train_dataset"
test_name = "test_dataset"

def make_noise(df, data_names):
    for data_name in data_names:
        min_signal = df[data_name].min()
        max_signal = df[data_name].max()
        gap = max_signal - min_signal

        gap *= NOISE_STD_DEVIATION 
        noise = np.random.normal(0, gap, df[data_name].shape)
        df[data_name] = df[data_name] + noise

    return df

def noise_csv(file_name):
    directory ="./"
    directory = directory+file_name
    filename = file_name+".csv"

    csv_list = []

    if filename.endswith(".csv"):
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)
        make_noise(df,DATA_NAMES)

        str_percent = str(PERCENT)
        df.to_csv(directory+'/'+file_name+'_noise'+str_percent+'.csv', index=False)