# -*- coding: utf-8 -*-
"""
Created on Wed May  6 10:22:27 2020

@author: MatelDS
"""

from pynput import mouse, keyboard
import time

def start_mouse_listener():
    global loc, mbutton  
    
    def mouse_update(x, y, button, pressed):      
        global loc, mbutton
        loc = (x,y)
        if button == mouse.Button.left:
            mbutton = "lmb"
        elif button == mouse.Button.right:
            mbutton = "rmb"
    
    loc = (0,0)
    mbutton = None
    
    mcontroller = mouse.Controller()
    mlistener = mouse.Listener(on_click=mouse_update)
    mlistener.start()
            
    return mcontroller, mlistener, loc, mbutton

def start_keyboard_listener():  
    global kkey
    
    def update_key(key):
        global kkey
        kkey = key
    
    kkey = None        
    kcontroller = keyboard.Controller()
    klistener = keyboard.Listener(on_press=update_key)
    klistener.start()
            
    return kcontroller, klistener, kkey

def stop_listener(listener):
    listener.stop()
    return True

def get_rloc(mcontroller, wndloc, resolution):
    '''returns relative mouse location.
    
    Input:
        wndloc - Tuple(x,y) of pixel coordinates of upper left window corner (Horizontal,Vertical)
        resolution - Tuple(x,y) of image resolution (Width,Height)
    
    Output:
        location - Tuple(x,y) with location relative to windowlocation and screensize.
            x and y are values between 0 and 1
            
    returns (0,0) when the cursor is outside of window area.'''
    
    loc = mcontroller.position
    x = (loc[0] - wndloc[0])/resolution[0]
    y = (loc[1] - wndloc[1])/resolution[1]
    
    if (x >= 0 and x<=1) and (y>=0 and y<=1):
        return (x,y)
    else:
        return (0,0)
    
def convert_loc_to_rloc(loc, wndloc, resolution):
    '''converts absolute mouse position to relative mouse position.
    
    Input:
        mloc - Tuple(x,y) absolute mouse position
        wndloc - Tuple(x,y) pixel coordinates of upper left window corner (Horizontal,Vertical)
        resolution - Tuple(x,y) image resolution (Width,Height)
    
    Output:
        location - Tuple(x,y) inside screen (relative) mouse location.
                x and y are values between 0 and 1
            
    returns (0,0) when the cursor is outside of window area.'''
    
    x = (loc[0] - wndloc[0])/resolution[0]
    y = (loc[1] - wndloc[1])/resolution[1]
    
    if (x >= 0 and x<=1) and (y>=0 and y<=1):
        return (x,y)
    else:
        return (0,0)
    
def convert_rloc_to_loc(rloc, wndloc, resolution):
    '''converts relative mouse position to absolute mouse position.
    
    Input:
        relmloc - Tuple(x,y) rinside screen (relative) mouse position
        wndloc - Tuple(x,y) pixel coordinates of upper left window corner (Horizontal,Vertical)
        resolution - Tuple(x,y) image resolution (Width,Height)
    
    Output:
        location - Tuple(x,y) absolute mouse location.
                x and y are values between 0 and 1
            
    returns (0,0) when the cursor is outside of window area.'''
    
    x = int(rloc[0]*resolution[0] + wndloc[0])
    y = int(rloc[1]*resolution[1] + wndloc[1])
    
    if (x >= 0 and x<=1) and (y>=0 and y<=1):
        return (x, y)
    else:
        return (0,0)

def listen_mk(duration, wndloc, resolution, allowedkeys=[]):
    '''listen for mouse and keyboard events and return last events after duration passed
    
    Input:
        duration - time to listen for events in seconds
        wndloc - Tuple(x,y) of pixel coordinates of upper left window corner (Horizontal,Vertical)
        resolution - Tuple(x,y) of image resolution (Width,Height)
        allowedkeys - list of strings. only keyboard inputs in this list will be recorded.
        
    Output:
        mevent - string. last occured Mouse-Event: "lmb", "rmb" or None
        rloc - Tuple(x,y) relative mouse position at time of last mouse-event. (0,0) if no mouse-event happened.
        kevent - string of last pressed key. None if no event occured'''
    global loc, mbutton, kkey
    loc = (0,0)
    mbutton, kkey = None, None
    
    rloc = (0,0)
    mevent = None
    kevent = None

    time.sleep(duration)
    
    if convert_loc_to_rloc(loc, wndloc, resolution) != (0,0):
        rloc = convert_loc_to_rloc(loc, wndloc, resolution)
        mevent = mbutton
    
    if len(allowedkeys)==0 or kkey in allowedkeys:
        kevent = kkey
    
    return mevent, rloc, kevent