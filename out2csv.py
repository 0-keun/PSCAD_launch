#! python3

import sys, os

from mhi.pscad.utilities.file import File
from mhi.pscad.utilities.file import OutFile

import win32com.client
import shutil
from csv_editor import add_class

# Working directory
working_dir = os.getcwd() + "\\"

# Create an Output folder called Results in the current directoty
result_folder = working_dir + "Results"
test_folder = working_dir + "test_dataset"
train_folder = working_dir + "train_dataset"

def clear_dir(dir):
    try:
        shutil.rmtree(dir)
        # print("Output folders are successfully cleared")
    except Exception as ignored:
        pass

def recreate_dir():
    try:
        shutil.rmtree(test_folder)
        shutil.rmtree(train_folder)
        # print("Output folders are successfully cleared")
    except Exception as ignored:
        pass

    if not os.path.exists(train_folder):
        os.makedirs(train_folder)
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)

def cvt_csv(iteration,goal,fault_type,start_time,end_time,num_type):
    # set constants
    threshold = (iteration+1) / goal
    event_start = (3*start_time+end_time)/4
    event_end = end_time
    fault_num = fault_type
    fault_location = str(fault_type//num_type)
    fault_type = str(int(fault_type % num_type))
    iteration = str(iteration+1)
    
    # test / train group
    if threshold > 0.7:
        data_folder = working_dir + "test_dataset"
    else:
        data_folder = working_dir + "train_dataset"

    # Save all data to output folder
    folder_result = os.path.join(result_folder)
    folder_data = os.path.join(data_folder)
    File.move_files(working_dir + "\pscad_model\ieee_39_bus.gf46", folder_result, ".out", ".inf") # load_the_data

    # Create a csv file of specific data channels between certain times
    out_file = OutFile(folder_result + "\\" + "noname")
    out_file.toCSV(start=start_time, end=end_time)

    # save a csv file
    # out_file.toCSV(columns=("Vrms_POC","P_POC","Q_POC"), start=start_time, end=end_time)
    os.rename(os.path.join(folder_result,"noname.csv"), os.path.join(folder_data,"output_location"+fault_location+"_type"+fault_type+"_ep"+iteration+".csv"))
    add_class(os.path.join(folder_data,"output_location"+fault_location+"_type"+fault_type+"_ep"+iteration+".csv"), fault_num, event_start, event_end)
    
    print('fault location: ' + fault_location + ', fault type: ' + fault_type + '\t['+iteration+'/'+str(goal)+']')