# -*- coding: utf-8 -*-
"""
Created on Wed May  6 14:46:54 2020

@author: Matel DS
"""
import pandas as pd
import os, time

from d2utilities.d2io import d2mouse, d2keyboard
from d2utilities.d2screen import d2screen

class d2session:
    def __init__(self, char="ama", splits=["den"], frameduration=0.25, wndname="Diablo II", dpiaware=False):
        self.char = char
        self.splits = splits
        self.duration = 0
        self.frameduration = frameduration
        self.wndname = wndname
        self.sessionnumber = None
        self.sessionloc = None
        self.dpiaware = dpiaware
        
        self.screen = d2screen(wndname=self.wndname, dpiaware=self.dpiaware)
        self.mouse = d2mouse(wndname=self.wndname, dpiaware=self.dpiaware)
        self.keyboard = d2keyboard()
        
    def add_minutes(self, minutes):
        self.duration = self.duration + minutes*60
        if self.duration<0:
            self.duration = 0
        print(f"recording duration: {self.duration/60:.2f}minutes")
        
    def add_seconds(self, seconds):
        self.duration = self.duration + seconds
        if self.duration<0:
            self.duration = 0
        print(f"recording duration: {self.duration:.0f}seconds")
            
    def set_frameduration(self, frameduration):
        self.frameduration = frameduration
        if self.frameduration <= 0:
            self.frameduration = 0.25
        
    def next_session(self):
        self.sessionnumber, self.sessionloc = self.create_folders(self.char, self.splits)
        
    def create_folders(self, char=None, splits=None):
        '''create folder structure for saving session data'''
        
        if char is None: char=self.char
        if splits is None: splits=self.splits
        
        session_number = 1
        sessionloc = os.getcwd()
        for f in ["data", self.char]:
            sessionloc = os.path.join(sessionloc, f)
            
        while os.path.exists(os.path.join(sessionloc, f"{session_number}")):
            session_number += 1
        
        sessionloc = os.path.join(sessionloc, f"{session_number}")
        for sp in splits:
            try:
                os.makedirs(os.path.join(sessionloc, sp, "imgs"))
            except:
                pass
    
        return session_number, sessionloc

    def capture_frame(self, start_listeners=False, stop_listeners=False):
        '''Takes a screenshot and listen for mouse and keyboard events (if listeners are running).
            
        Output (Image, image_size, mkactions):
            Image - PIL image of the screenshot taken.
            image_size - Tuple(Width,Height) size of the image
            mkactions - dictionary with last event of {"mouse", "mouselocation", "keyboard"}'''
        
        error, image, image_size, wndloc, wndsize = self.screen.get_screen()
        
        if start_listeners:
            self.mouse.start_listener(), self.keyboard.start_listener()
        
        self.mouse.reset(), self.keyboard.reset()
        time.sleep(self.frameduration)
        
        mevent = self.mouse.mbutton
        rloc = self.mouse.rloc
        kevent = self.keyboard.kkey
        
        if stop_listeners:
            self.mouse.stop_listener(), self.keyboard.stop_listener()

        mkactions = {"mouse":mevent, "mouse_x":rloc[0], "mouse_y":rloc[1], "keyboard":kevent}
        
        return image, image_size, mkactions
        
    def record_for_duration(self, split):
        
        '''records a gaming session for time duration.
        
        Use d2session.record_all_splits() to start a recording session'''
        
        try:
            print(f"Start recording of split '{split}' for {self.duration/60:.2f} minutes.")
            input_data = pd.DataFrame(columns=["mouse", "mouse_x","mouse_y", "keyboard"])
            
            self.mouse.start_listener(), self.keyboard.start_listener()
        
            t_end = time.time()+self.duration
            frame = 0
            while time.time()<t_end:
                image, image_size, mkactions = self.capture_frame()
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
        
    def record_all_splits(self):
        '''record all splits in succession'''
        self.next_session()
        for split in self.splits:
            err = self.record_for_duration(split)
        
        return err