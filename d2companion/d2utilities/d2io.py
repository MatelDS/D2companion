# -*- coding: utf-8 -*-
"""
Created on Wed May  6 10:22:27 2020

@author: MatelDS
"""

from pynput import mouse, keyboard
from d2screen import d2screen

class d2mouse:
    def __init__(self, wndname="Diablo II", dpiaware=False):                
        self.controller = mouse.Controller()
        self.mbutton = None
        self.loc = (0,0)
        self.rloc = (0,0)
        self.wndname = "Diablo II"
        self.dpiaware = dpiaware
        self.mscreen = d2screen(self.wndname, dpiaware=self.dpiaware)
        self.update_window_position()

    def start_listener(self):     
        def mouse_update(x, y, button, pressed):
            self.loc = (x,y)            
            self.update_window_position()
            if self.get_rloc() != (0,0):
                self.rloc = self.get_rloc()
                if button == mouse.Button.left:
                    self.mbutton = "lmb"
                elif button == mouse.Button.right:
                    self.mbutton = "rmb"

        self.listener = mouse.Listener(on_click=mouse_update)
        self.listener.start()
    
    def stop_listener(self):
        self.listener.stop()
        
    def reset(self):
        self.mbutton = None
        self.loc = (0,0)
        self.rloc = (0,0)
        
    def update_window_position(self):
        self.wndloc, self.wndsize = self.mscreen.get_window_location()
        
    def get_rloc(self):
        '''returns relative mouse location (inside gamescreen area).
        
        Output:
            location - Tuple(x,y) with location relative to windowlocation and screensize.
                returns (0,0) when the cursor is outside of window area.'''
        
        x = (self.loc[0] - self.wndloc[0])/self.wndsize[0]
        y = (self.loc[1] - self.wndloc[1])/self.wndsize[1]
        
        if (x >= 0 and x<=1) and (y>=0 and y<=1):
            return (x,y)
        else:
            return (0,0)
        
    def convert_loc_to_rloc(self, loc):
        '''converts absolute mouse position to relative mouse position.
        
        Input:
            mloc - Tuple(x,y) absolute mouse position
        
        Output:
            location - Tuple(x,y) inside screen (relative) mouse location.
                    x and y are values between 0 and 1
                
                returns (0,0) when the cursor is outside of window area.'''
                
        x = (loc[0] - self.wndloc[0])/self.wndsize[0]
        y = (loc[1] - self.wndloc[1])/self.wndsize[1]
        
        if (x >= 0 and x<=1) and (y>=0 and y<=1):
            return (x,y)
        else:
            return (0,0)
    
    def convert_rloc_to_loc(self, rloc):
        '''converts relative mouse position to absolute mouse position.
        
        Input:
            relmloc - Tuple(x,y) rinside screen (relative) mouse position
            wndloc - Tuple(x,y) pixel coordinates of upper left window corner (Horizontal,Vertical)
            resolution - Tuple(x,y) image resolution (Width,Height)
        
        Output:
            location - Tuple(x,y) absolute mouse location.
                    x and y are values between 0 and 1
                
        returns (0,0) when the cursor is outside of window area.'''
        
        x = int(rloc[0]*self.wndsize[0] + self.wndloc[0])
        y = int(rloc[1]*self.wndsize[1] + self.wndloc[1])
        
        if (x >= 0 and x<=1) and (y>=0 and y<=1):
            return (x, y)
        else:
            return (0,0)
        
    def check_functionality(self): 
        def on_move(x, y):
            self.update_window_position()
            print(f"loc:({x},{y}); rloc:{self.convert_loc_to_rloc((x,y))}")
            
        self.listener = mouse.Listener(on_move=on_move)
        self.listener.start()
        
class d2keyboard:
    def __init__(self, allowedkeys=[]):              
        self.controller = keyboard.Controller()
        self.allowedkeys = allowedkeys
        self.kkey = None
        
    def start_listener(self):  
        def update_key(key):
            key_value = None
            
            if key is None:
                pass
            else:
                try:
                    key_value = key.char
                except:
                    key_value = key.name
                finally:
                    if len(self.allowedkeys)==0 or key_value in self.allowedkeys:
                        self.kkey = key_value

        self.listener = keyboard.Listener(on_press=update_key)
        self.listener.start()

    def stop_listener(self):
        self.listener.stop()
        
    def reset(self):
        self.kkey = None
    
    def reset_allowedkeys(self):
        self.allowedkeys = []
        
    def allow_keys(self, *args):
        for item in args:
            if type(item) is str:
                self.allowedkeys.append(item)
            
            elif type(item) is list:
                for litem in item:
                    if type(litem) is str:
                        self.allowedkeys.append(litem)