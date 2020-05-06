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

minutes = 10
frameduration = 0.25

char = "ama"
sessionNR = 1
split = "den"

folders = ["data", f"{char}", f"{sessionNR}", f"{split}"]
saveloc = os.getcwd()
for f in folders:
    saveloc = os.path.join(saveloc, f)

imgloc = os.path.join(saveloc, "imgs")

try:
    os.makedirs(imgloc)
except:
    pass

df = pd.DataFrame(columns=["mouse", "mouse_x","mouse_y", "keyboard"])
imgs = pd.DataFrame(columns=["Image"])

mcontroller, mlistener, loc, mbutton = d2io.start_mouse_listener()
kcontroller, klistener, kkey = d2io.start_keyboard_listener()

t_end = time.time()+minutes*60
i=0
while time.time()<t_end:
    image, image_size, mkactions = capture_frame(frameduration)
    df = df.append(mkactions, ignore_index=True)
    image.save(os.path.join(imgloc, f"{i}.jpeg"))
    #imgs = imgs.append({"Image":image}, ignore_index=True)
    i = i+1
    
d2io.stop_listener(mlistener)
d2io.stop_listener(klistener)
    
df.to_csv(os.path.join(saveloc, f"{split}.csv"))