# PSCAD_launch

# tested environment

python==3.8.0, CUDA==11.8, cudnn==8.6.0, tensorflow==2.10.0  

PSCAD==5.0.1 with "mhi" library, not "mhrc"

# simulation
## related files
pscad_model, csv_editor.py, out2csv.py, run_simulation.py  

## how to run
- create snapshot file  
    1. Launch the PSCAD file (ieee_39_bus_system in the pscad_model folder)
    2. Set the project setting,
    <br/>
    ![image](https://github.com/user-attachments/assets/5c0dae6a-a29c-4204-ab78-34b2faad77d5)

    4. Run simulation and get snapshot file.
    
    
- run the simulation
    1. Change project setting,
    <br/>
    ![image](https://github.com/user-attachments/assets/e153d8ec-3b3d-45d8-bd04-675c8c23bea5)



    3. Save and close the window.
    4. Run python file.
    ```bash
    python run_simulation.py
    ```

# LSTM
## related files
train_LSTM.py, train_LSTM_multiple.py, test_LSTM.py, test_realtime.py  

## training
- If you are using single GPU, use this.
    ```bash
    train_LSTM.py
    ```
- If you are using multiple GPUs, use this.
    ```bash
    train_LSTM_multiple.py
    ```

## testing
- testing for accuracy
    ```bash
    test_LSTM.py
    ```
- testing for execution time and frequency
    ```bash
    test_realtime.py
    ```
