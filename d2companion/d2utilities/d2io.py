# -*- coding: utf-8 -*-
"""
Created on Wed May  6 10:22:27 2020

@author: MatelDS
"""

import win32ui, win32gui
from pynput import mouse, keyboard
from ctypes import windll
from PIL import Image

class d2screen:
    def __init__(self, wndname="Diablo II", dpiaware=False, dpiaware_wndsize=(646,509)):
        self.wndname = wndname
        self.onlyarea = False
        self.update_window_location()
        if self.onlyarea:
            self.real_wndsize = dpiaware_wndsize #(640,480)
        else:
            self.real_wndsize = dpiaware_wndsize #(646,509)
        
        self.dpiaware = dpiaware
        #set DPI awareness in windows
        #can solve issue of different mouse controller and listener coordinates
        #on High DPI devices. Nevertheless the handling becomes dirty and may
        #cause issues with the screen-capture output.
        if self.dpiaware:
            PROCESS_PER_MONITOR_DPI_AWARE = 2
            windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
        
    def update_window_location(self):
        '''updates current location of client window.'''
        hwnd = win32gui.FindWindow(None, self.wndname)
        hwndDC = win32gui.GetWindowDC(hwnd)

        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        #cleft, ctop, cright, cbot = win32gui.GetClientRect(hwnd)

        w = right - left
        h = bot - top
        
        #cw = cright - cleft
        #ch = cbot - ctop
        
        win32gui.ReleaseDC(hwnd, hwndDC)
        
        self.wndloc = (left,top)
        self.wndsize = (w, h)
        
    def get_window_location(self):
        '''returns current window location'''
        self.update_window_location()
        
        return self.wndloc, self.wndsize

    def get_screen(self):
        '''Make Screenshot of running window.
        
        Returns (Error, Imagesize, Image)
            Error - Boolean
            Image - PIL-Image object
            Imagesize - Tuple(x,y) size of the image in form (Width,Height)
            windowlocation - Tuple(x,y) location of the upper left window corner
            '''
        
        try:
            hwnd = win32gui.FindWindow(None, self.wndname)
    
            left, top, right, bot = win32gui.GetWindowRect(hwnd)
            cleft, ctop, cright, cbot = win32gui.GetClientRect(hwnd)
            
            w = right - left
            h = bot - top
    
            cw = cright - cleft
            ch = cbot - ctop
            
            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            
            saveBitMap = win32ui.CreateBitmap()
            if self.onlyarea:
                saveBitMap.CreateCompatibleBitmap(mfcDC, cw, ch)
            else:
                saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
            
            saveDC.SelectObject(saveBitMap)
            
            #whole window or just the client area.
            if self.onlyarea:
                result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
            else:
                result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
            
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            
            self.image = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1)
            if self.dpiaware:
                self.image = self.image.crop((0,0,self.real_wndsize[0], self.real_wndsize[1]))
                        
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwndDC)
            
            self.imsize = (self.image.width, self.image.height)
            self.wndloc = (left,top)
            self.wndsize = (w, h)
            
        except:
            result = 0
            print("Error while getting Screen.")
            
        finally:
            if result == 1:
                #PrintWindow succeeded, return error=False
                return False, self.image, self.imsize, self.wndloc, self.wndsize
            
            else:
                #PrintWindow failed, return error=True
                return True, None, (0,0), (0,0), (640,480)

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