# PSCAD_launch

# tested environment

python==3.8.0, CUDA==11.8, cudnn==8.6.0, tensorflow==2.10.0  

PSCAD==5.0.1 with "mhi" library, not "mhrc"

# simulation
## related files
pscad_model, csv_combined.py, make_noise.py, out2csv.py, run_simulation.py  

## how to run
- download PSCAD models  
    download projects to the pscad model directory.
    
- run the simulation
    ```bash
    python run_simulation.py
    ```
- edit csv files
    You have to combine the output files for training.
    ```bash
    csv_combine.py
    ```
    Generating noises makes training more practical.
    ```bash
    make_noise.py
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
