# -*- coding: utf-8 -*-
"""
Created on Wed May  6 14:46:54 2020

@author: Matel DS
"""
import pandas as pd
import os, time

import d2io
import d2screenutils as d2su

def capture_frame(duration):
    '''Takes a screenshot and listen for mouse and keyboard events.
    
    Input:
        duration - float. Time to listen after taking screenshot.
        
    Output (Image, mkactions):
        Image - PIL image of the screenshot taken.
        mkactions - dictionary with last event of {"mouse", "mouselocation", "keyboard"}'''
    
    error, image, image_size, wndloc = d2su.get_screen(wndname="Diablo II", onlyarea=True)
    
    mevent, rloc, kevent = d2io.listen_mk(duration, wndloc=wndloc, resolution=image_size)
    mkactions = {"mouse":mevent, "mouse_x":rloc[0], "mouse_y":rloc[1], "keyboard":kevent}
    
    return image, image_size, mkactions

def create_folders(char="ama", splits=["den"]):
    '''create folder structure for saving session data'''
    
    session_number = 1
    sessionloc = os.getcwd()
    for f in ["data", char]:
        sessionloc = os.path.join(sessionloc, f)
        
    while os.path.exists(os.path.join(sessionloc, f"{session_number}")):
        session_number += 1
    
    sessionloc = os.path.join(sessionloc, f"{session_number}")
    for sp in splits:
        try:
            os.makedirs(os.path.join(sessionloc, sp, "imgs"))
        except:
            pass
    
    return sessionloc

def record_timed_split(minutes, seconds, sessionloc, frameduration=0.25, split = "den"):
    '''records a gaming session for given time duration'''
    
    try:
        input_data = pd.DataFrame(columns=["mouse", "mouse_x","mouse_y", "keyboard"])
        
        mcontroller, mlistener, loc, mbutton = d2io.start_mouse_listener()
        kcontroller, klistener, kkey = d2io.start_keyboard_listener()
    
        t_end = time.time()+minutes*60+seconds
        frame = 0
        while time.time()<t_end:
            image, image_size, mkactions = capture_frame(frameduration)
            input_data = input_data.append(mkactions, ignore_index=True)
            image.save(os.path.join(sessionloc, split, "imgs", f"{frame}.jpeg"))
            frame += 1
    
        d2io.stop_listener(mlistener)
        d2io.stop_listener(klistener)
    
        input_data.to_csv(os.path.join(sessionloc, split, "input.csv"))
        
        return False
    
    except:
        return True

minutes = 5
seconds = 0
frameduration = 0.25

char = "assa"
splits = ["den"]

sessionloc = create_folders(char, splits)

for split in splits:
    err = record_timed_split(minutes, seconds, sessionloc, frameduration, split)
    
if err:
    print("Error: Session stoped.")
else:
    print(f"Recording completed./n The data was saved in/n {sessionloc}")