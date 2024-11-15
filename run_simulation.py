#!/usr/bin/env python3

import mhi.pscad
import out2csv
import os
import math
import mhi.pscad.handler
import random
import time
import csv_editor

# ETA = NUM_EP*NUM_TYPE*num_location*simul_time

class DATA_GENERATOR():
    def __init__(self):
        # Parameters
        self.NUM_EP                 = 30
        self.TIME_STEP              = 25  #[us]
        self.REC_START              = 3.0 #[s]
        self.REC_END                = 3.20 #[s]
        self.SNAP_TIME              = 3.0 #[s]
        self.EVENT_DURATION         = 0.050 # 0.050 #[s]
        self.NUM_TYPE               = 4

        # Fault_location
        self.fault_sliders = [2093508710,1683108412,655794188,465722641,344768387,
                              2103561458,1719687809,347290643,822615222,1527581778,
                              191371636,1692252608,1485504637,1948285602,1525328006,
                              1386218942,242459496,200978327,363413007,1517486302,
                              778078859,1352194669,2040702627,1692752872,403456664,
                              104868247,431362582,1378127936,433693825,204450919,
                              379111274,1146702036,924153973,1351327130]
        
        self.fault_timers  = [1462212716,483027746,1405299315,2093158134,2011283344,
                              326438324,1793686934,2055444510,1156058832,1273406862,
                              441710515,2118506576,3438412,1811758467,458109167,
                              301285391,1808037142,701716425,1096875049,1093726691,
                              700019167,59935488,934983485,606981510,1220729841,
                              651641648,39790737,370916838,138760033,1411499999,
                              1761070132,2006928665,1393573637,188082429]

        self.num_location = len(self.fault_sliders)
        self.prev_location = -1
        self.prev_time = time.time()

        # Working directory
        working_dir = os.getcwd() + "\\"

        # Create an Output folder called Results in the current directoty
        self.result_folder = working_dir + "Results"

        # recreate Data folder
        out2csv.recreate_dir()

        # set up
        self.settings = { 'fortran_version': 'GFortran 4.6.2' }
        self.pswx_path = r"./pscad_model/ieee_39_bus_system.pswx"
        self.project_1 = 'ieee_39_bus'

        # Launch specific PSCAD and Fortran version
        self.pscad = mhi.pscad.launch(version='5.0.1', settings=self.settings)
        with mhi.pscad.application() as self.pscad:
            self.pscad.load(self.pswx_path)
            self.project = self.pscad.project(self.project_1)
            self.project.parameters(time_duration=self.REC_END-self.SNAP_TIME) #, Mruns=5)
            self.reset_components()

    def reset_components(self):
        if self.prev_location == -1:
            for i in range(len(self.fault_sliders)):
                # slider
                self.fault_slider = self.project.component(self.fault_sliders[i])
                self.fault_slider.parameters(Value='0')
        else: 
            self.fault_slider = self.project.component(self.fault_sliders[self.prev_location])
            self.fault_slider.parameters(Value='0')
        
    def fault_generator(self, f_type):
        # reset
        self.reset_components()
        fault_location = int(f_type // self.NUM_TYPE)
        fault_type = int(f_type % self.NUM_TYPE)

        # generate event while recording.
        event_start = random.uniform(self.REC_START+self.EVENT_DURATION, self.REC_END-self.EVENT_DURATION)
        event_duration = self.EVENT_DURATION

        # set slider, timer
        self.fault_slider = self.project.component(self.fault_sliders[fault_location])
        self.fault_slider.value(fault_type)
        self.fault_timer = self.project.component(self.fault_timers[fault_location])
        self.fault_timer.parameters(TF=str(event_start), DF=str(event_duration))

        self.prev_location = fault_location

        return event_start, event_duration

    # load and run the simulation
    def run_sim(self, fault_type):
        for i in range(self.NUM_EP):
            out2csv.clear_dir(self.result_folder)

            # fault gen and run
            event_start, event_duration = self.fault_generator(fault_type)
            self.project.run()

            fault_rec_start = event_start - event_duration/3
            fault_rec_end = event_start + event_duration

            print("================================================")
            out2csv.cvt_csv(i, self.NUM_EP, fault_type, fault_rec_start, fault_rec_end, self.NUM_TYPE)
            
            self.current_time = time.time()
            # print('simulation_time: ',self.current_time-self.prev_time)
            eta = (self.NUM_TYPE*self.num_location*self.NUM_EP)*(self.current_time-self.prev_time) - (fault_type*self.NUM_EP + i)*(self.current_time-self.prev_time)
            rate = ((fault_type*self.NUM_EP + i) * 100) / (self.NUM_TYPE*self.num_location*self.NUM_EP)
            print("ETA: ",str(math.floor(eta/3600))+":"+str(math.floor((eta%3600)/60)).rjust(2,'0')+":"+str(math.floor(eta%60)).rjust(2, '0'),"  -  ",str(round(rate,2))+"%")
            self.prev_time = time.time()

    def main(self):
        with mhi.pscad.application() as self.pscad:
            self.pscad.load(self.pswx_path)
            self.project = self.pscad.project(self.project_1)
            self.project.parameters(time_duration=self.REC_END-self.SNAP_TIME,time_step=self.TIME_STEP)

            for i in range(self.NUM_TYPE*self.num_location):
                if (i%self.NUM_TYPE)!=0 or i==0:
                    self.run_sim(fault_type=i)
                else:
                    pass

        csv_editor.combine_csv("train_dataset")
        csv_editor.combine_csv("test_dataset")

        csv_editor.noise_csv("train_dataset")
        csv_editor.noise_csv("test_dataset")

if __name__ == '__main__':
    data_generator = DATA_GENERATOR()
    data_generator.main()