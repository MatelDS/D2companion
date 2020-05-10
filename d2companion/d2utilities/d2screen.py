# -*- coding: utf-8 -*-
"""
Created on Mon May  4 07:03:29 2020

@author: MatelDS
"""
import win32gui
import win32ui
from ctypes import windll
from PIL import Image

class d2screen:
    def __init__(self, wndname="Diablo II", dpiaware=False):
        self.wndname = wndname
        self.onlyarea = False
        self.update_window_location()
        if self.onlyarea:
            self.real_wndsize = (640,480)
        else:
            self.real_wndsize= (646,509)
        
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