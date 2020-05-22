# -*- coding: utf-8 -*-
"""
Created on Wed May  6 14:46:54 2020

@author: Matel DS
"""
import pandas as pd
import os, time, threading

from d2utilities.d2io import D2Screen, D2Mouse, D2Keyboard

class d2recordsession:
    def __init__(self, char="ama", splits=["den"], frameduration=0.1,
                 wndname="Diablo II",
                 dpiaware=False, dpiaware_wndsize=(646,509)):
        self.char = char
        self.splits = splits
        self.duration = 0
        self.max_duration = 1 *60 *60 #1 hour
        self.frameduration = frameduration
        self.wndname = wndname
        self.update_session()
        self.dpiaware = dpiaware
        self.recording = None
        
        self.screen = D2Screen(wndname=self.wndname, dpiaware=self.dpiaware,
                               dpiaware_wndsize=dpiaware_wndsize)
        self.mouse = D2Mouse(wndname=self.wndname, dpiaware=self.dpiaware)
        self.keyboard = D2Keyboard()
        
    def add_minutes(self, minutes):
        '''add minutes to recording duration'''
        self.duration = self.duration + minutes*60
        if self.duration<0:
            self.duration = 0
        print(f"recording duration: {self.duration/60:.2f}minutes")
        
    def add_seconds(self, seconds):
        '''add seconds to recording duration'''
        self.duration = self.duration + seconds
        if self.duration<0:
            self.duration = 0
        print(f"recording duration: {self.duration:.0f}seconds")
        
    def set_recording_duration(self, new_duration):
        '''set time for recording session'''
        self.duration = new_duration
        if self.duration<0:
            self.duration = 0
        print(f"recording duration: {self.duration:.0f}seconds")      
            
    def set_frameduration(self, frameduration):
        '''set time duration of recorded frames'''
        self.frameduration = frameduration
        if self.frameduration <= 0:
            self.frameduration = 0.25
            
    def set_splits(self, new_splits=["den"]):
        '''set list of splits'''
        self.splits = new_splits
        
    def get_splits(self):
        '''get current list of split-names'''
        return self.splits
    
    def add_split(self, split):
        '''add a split to split list'''
        
        
    def update_session(self):
        '''updates current sessionnumber'''        
        self.session_number = 1
        self.sessionloc = os.getcwd()
        for f in ["data", self.char]:
            self.sessionloc = os.path.join(self.sessionloc, f)
            
        while os.path.exists(os.path.join(self.sessionloc, f"{self.session_number}")):
            self.session_number += 1
            
        self.sessionloc = os.path.join(self.sessionloc, f"{self.session_number}")
        
    def create_folders(self, splits=None, update_session=True):
        '''create folder structure for saving session data'''                
        if update_session:
            self.update_session()
        
        if splits is None:
            splits = self.splits
        for sp in splits:
            try:
                os.makedirs(os.path.join(self.sessionloc, sp, "imgs"))
            except:
                pass

    def capture_frame(self, t_start, start_listeners=False, stop_listeners=False,
                      create_folders=False):
        '''Takes a screenshot and listen for mouse and keyboard events (if listeners are running).
            
        Output (Image, image_size, mkactions):
            Image - PIL image of the screenshot taken.
            image_size - Tuple(Width,Height) size of the image
            mkactions - dictionary with last event of {"mouse", "mouselocation", "keyboard"}'''
        
        error, image, image_size, wndloc, wndsize = self.screen.get_screen()
        
        if create_folders:
            self.mouse.start_listener(), self.keyboard.start_listener()
            
        if start_listeners:
            self.mouse.start_listener(), self.keyboard.start_listener()
        
        time.sleep(self.frameduration)
        
        mevent = self.mouse.mbutton
        rloc = self.mouse.rloc
        kevent = self.keyboard.kkey
        ftime = time.time()-t_start
        self.mouse.reset(), self.keyboard.reset()
        
        if stop_listeners:
            self.mouse.stop_listener(), self.keyboard.stop_listener()

        mkactions = {"time":ftime, "mouse":mevent, "mouse_x":rloc[0], "mouse_y":rloc[1], "keyboard":kevent}
        
        return image, image_size, mkactions
        
    def record_for_duration(self, split="timed"):        
        '''records a gaming session for time duration.'''       
        try:
            print(f"Start recording of split '{split}' for {self.duration/60:.2f} minutes.")
            input_data = pd.DataFrame(columns=["time", "mouse", "mouse_x","mouse_y", "keyboard"])
            
            self.mouse.start_listener(), self.keyboard.start_listener()
            self.create_folders([split])
            
            t_start = time.time()
            t_end = t_start+self.duration
            frame = 0
            while time.time()<t_end:
                image, image_size, mkactions = self.capture_frame(t_start)
                input_data = input_data.append(mkactions, ignore_index=True)
                image.save(os.path.join(self.sessionloc, split, "imgs", f"{frame}.jpeg"))
                frame += 1
        
            self.mouse.stop_listener(), self.keyboard.stop_listener()
            
            input_data.to_csv(os.path.join(self.sessionloc, split, "input.csv"))
            print(f"Recording finished. Data Saved.")
            
            return False
    
        except:
            print(f"Error while recording. Data of Session {self.sessionnumber}/{split} may be incomplete.")
            return True
        
    def record_all_splits_timed(self):
        '''record all splits in succession'''
        self.create_folders()
        for split in self.splits:
            self.record_for_duration(split=split)
    
    def start_recording(self, split="den", duration=None, new_session=True):
        '''Start recording. Needs to be stopped with .stop_recording() method.
        Recording Time limited by max_duration value.'''
        
        class RecordThread(threading.Thread):
            """Thread class with a stop() method. The thread itself has to check
            regularly for the stopped() condition."""
        
            def __init__(self, *args, **kwargs):
                super(RecordThread, self).__init__(*args, **kwargs)
                self._stop = threading.Event()
        
            def stop(self):
                self._stop.set()
        
            def stopped(self):
                return self._stop.isSet()
        
        self.input_data = pd.DataFrame(columns=["time", "mouse", "mouse_x","mouse_y", "keyboard"])

        self.current_split = split
        
        self.mouse.start_listener(), self.keyboard.start_listener()
        self.create_folders(splits=[split], update_session=new_session)
        
        if duration is not None:        
            self.recording = RecordThread(target=self.__capt_imgs_timed, daemon=True)
        else:
            self.recording = RecordThread(target=self.__capt_imgs, daemon=True)
            
        self.recording.start()
        
    def __capt_imgs(self):
        frame = 0
        t_start = time.time()
        t_end = t_start+self.max_duration
        while time.time()<t_end and not self.recording.stopped():
            image, image_size, mkactions = self.capture_frame(t_start)
            self.input_data = self.input_data.append(mkactions, ignore_index=True)
            image.save(os.path.join(self.sessionloc, self.current_split, "imgs", f"{frame}.jpeg"))
            frame += 1
        
        if not self.recording.stopped():
            self.stop_recording()
            
    def __capt_imgs_timed(self):
        frame = 0
        t_start = time.time()
        t_end = t_start+self.duration
        while time.time()<t_end and not self.recording.stopped():
            image, image_size, mkactions = self.capture_frame(t_start)
            self.input_data = self.input_data.append(mkactions, ignore_index=True)
            image.save(os.path.join(self.sessionloc, self.current_split, "imgs", f"{frame}.jpeg"))
            frame += 1
            
        if not self.recording.stopped():
            self.stop_recording()
        
    def stop_recording(self):
        '''stop recording and save input.csv'''
        if self.recording is None:
            print("No recording running.")
        elif not self.recording.stopped():
            self.recording.stop()
            time.sleep(self.frameduration*2)
            self.mouse.stop_listener(), self.keyboard.stop_listener()
            self.input_data.to_csv(os.path.join(self.sessionloc, self.current_split, "input.csv"))            
            self.input_data = pd.DataFrame(columns=["time", "mouse", "mouse_x","mouse_y", "keyboard"])
            print(f"Recording finished. Data Saved.")
        else:
            try:
                self.recording.stop()
                time.sleep(self.frameduration*2)
                self.mouse.stop_listener(), self.keyboard.stop_listener()
                self.input_data.to_csv(os.path.join(self.sessionloc, self.current_split, "input.csv"))            
                self.input_data = pd.DataFrame(columns=["time", "mouse", "mouse_x","mouse_y", "keyboard"])
            finally:
                print(f"Recording finished. Data Saved.")
            
    def stopped(self):
        '''check if recording has stopped'''
        if self.recording == None:
            return True
        else:
            return self.recording.stopped()
        