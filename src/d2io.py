# -*- coding: utf-8 -*-
"""
Created on Wed May  6 10:22:27 2020

@author: MatelDS
"""

import mouse
import keyboard
import time

def getMloc(wndloc, resolution):
    '''returns relative mouse location.
    
    Input:
        wndloc - Tuple(x,y) of pixel coordinates of upper left window corner (Horizontal,Vertical)
        resolution - Tuple(x,y) of image resolution (Width,Height)
    
    Output:
        location - Tuple(x,y) with location relative to windowlocation and screensize.
            x and y are values between 0 and 1
            
    returns (0,0) when the cursor is outside of window area.'''
    
    loc = mouse.get_position()
    x = (loc[0] - wndloc[0])/resolution[0]
    y = (loc[1] - wndloc[1])/resolution[1]
    
    if (x >= 0 and x<=1) and (y>=0 and y<=1):
        return (x,y)
    else:
        return (0,0)
    
def Mmove(target, wndloc, resolution):
    '''Moves Mouse to target Screen Location
    
    Input:
        target - Tuple(x,y) of relative coordinates (Width,Height):values between 0 and 1
        wndloc - Tuple(x,y) of pixel coordinates of upper left window corner (Horizontal,Vertical)
        resolution - Tuple(x,y) of image resolution (Width,Height)
    Output:
        error - boolean'''
        
    x = int(target[0]*resolution[0] + wndloc[0])
    y = int(target[1]*resolution[1] + wndloc[1])
    
    if (x<0 or x>1) or (y<0 or y>1):
        error = True
    else:    
        try:
            mouse.move(x,y, absolute=True)
            error = False
            
        except:
            error = True
        
    return error

def Mlisten(duration, wndloc, resolution):
    '''listen for mouse events and return last event after duration passed
    
    Input:
        duration - time to listen for events in seconds
        wndloc - Tuple(x,y) of pixel coordinates of upper left window corner (Horizontal,Vertical)
        resolution - Tuple(x,y) of image resolution (Width,Height)
        
    Output:
        mevent - string of last occured Mouse-Event: "lmb", "rmb" or None
        mloc - Tuple(x,y) of mouse position at time of last mouse-event. (0,0) if no mouse-event happened.'''
    
    mloc = (0,0)
    mevent = None
    
    t_end = time.time() + duration
    while time.time() < t_end:
        if mouse.is_pressed(button="left"):
            loc = getMloc(wndloc, resolution)
            if loc != (0,0):
                mevent = "lmb"
                mloc = loc
                
        if mouse.is_pressed(button="right"):
            loc = getMloc(wndloc, resolution)
            if loc != (0,0):
                mevent = "rmb"
                mloc = loc
    
    return mevent, mloc

def MKlisten(duration, wndloc, resolution):
    '''listen for mouse and keyboard events and return last events after duration passed
    
    Input:
        duration - time to listen for events in seconds
        wndloc - Tuple(x,y) of pixel coordinates of upper left window corner (Horizontal,Vertical)
        resolution - Tuple(x,y) of image resolution (Width,Height)
        
    Output:
        mevent - string of last occured Mouse-Event: "lmb", "rmb" or None
        mloc - Tuple(x,y) of mouse position at time of last mouse-event. (0,0) if no mouse-event happened.
        kevent - string of last pressed key. None if no event occured'''
    
    mloc = (0,0)
    mevent = None
    
    t_end = time.time() + duration
    keyboard.start_recording()
    while time.time() < t_end:
        if mouse.is_pressed(button="left"):
            loc = getMloc(wndloc, resolution)
            if loc != (0,0):
                mevent = "lmb"
                mloc = loc
                
        if mouse.is_pressed(button="right"):
            loc = getMloc(wndloc, resolution)
            if loc != (0,0):
                mevent = "rmb"
                mloc = loc
    
    kevents = keyboard.stop_recording()
    
    if len(kevents) == 0:
        kevent = None
    else:
        kevent = kevents[-1].name
    
    return mevent, mloc, kevent

def Klisten(duration):
    '''listen for keyboard events and return last event after duration passed
    
    Input:
        duration - time to listen for events in seconds
        
    Output:
        event - string of last key pressed
        
    returns None if no event occured'''
    
    t_end = time.time() + duration
    keyboard.start_recording()
    while time.time() < t_end:
        pass
    events = keyboard.stop_recording()
    
    if len(events) == 0:
        return None
    else:
        event = events[-1].name
        return event
    
def Kinput(key, allowedkeys=[]):
    '''simple keyboard event
    
    Input:
        key - string of pressed button on keyboard
        allowedkeys - list of keys that are allowed to be pressed. Empty list means no key restrictions.
        
    Output:
        error - boolean'''
        
    try:
        if len(allowedkeys) == 0:
            keyboard.send(key)
            
        else:
            if key in allowedkeys:
                keyboard.send(key)
                
        return False
            
    except:
        return True
    
duration = 5
wndloc = (0,0)
resolution = (1920,1024)
time.sleep(1)
print(Mlisten(duration, wndloc, resolution))