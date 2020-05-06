# -*- coding: utf-8 -*-
"""
Created on Mon May  4 07:03:29 2020

@author: MatelDS
"""
import win32gui
import win32ui
from ctypes import windll
from PIL import Image

def getScreen(wndname="Diablo II"):
    '''Make Screenshot of running window.
    Input: wndname - String of Windowname
    
    Returns (Error, Imagesize, Image)
        Error - Boolean
        Imagesize - Tuple(width,Height)
        Image - PIL-Image object'''
    
    try:
        hwnd = win32gui.FindWindow(None, 'Diablo II')
        
        # Change the line below depending on whether you want the whole window
        # or just the client area. 
        left, top, right, bot = win32gui.GetClientRect(hwnd)
        #left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top
        
        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        
        saveDC.SelectObject(saveBitMap)
        
        # Change the line below depending on whether you want the whole window
        # or just the client area. 
        result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
        #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
        #print(result)
        
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        
        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
        
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)
        
        imsize = (im.width, im.height)
    except:
        result = 0
        print("Error while taking Screenshot.")
        
    finally:
        if result == 1:
            #PrintWindow Succeeded, return Image and Size
            return False, imsize, im
        
        else:
            #PrintWindow failed, return error=True
            return True, (0,0), None