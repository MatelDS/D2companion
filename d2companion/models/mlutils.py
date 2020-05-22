# -*- coding: utf-8 -*-

"""
Created on Thu May  7 18:37:37 2020

@author: MatelDS
"""

import os

import numpy as np
import pandas as pd
from PIL import Image
from pathlib import Path

searchpath = "C:\\PyCode\\Projects\\D2companion\\data"

class d2DataSet:
    def __init__(self):
        self.imglist = []
        self.mainpath = Path(os.getcwd())

    def set_path(self, mainpath):
        '''set path for located images'''
        self.mainpath = Path(mainpath)
        
    def find_images(self, fileformat=".jpeg", inplace=True):
        '''find all files of given data format'''
        newlist = []
        for path in Path(self.mainpath).rglob("*"+fileformat):
                newlist.append(path)
        if inplace:
            self.imglist = newlist
        else:
            return newlist
    
    def filter_imgs(self, pattern, imglist=None, inplace=True):
        '''select only images with given str-pattern from list of filepaths'''
        if imglist is None:
            imglist = self.imglist
            
        newlist = [k for k in imglist if pattern in str(k)]
        if inplace:
            self.imglist = newlist
        else:
            return newlist
        
    def update_index(self):
        '''updates indices of all images in imglist'''
        self.char = [c.parts[-5] for c in self.imglist]
        self.session = [int(c.parts[-4]) for c in self.imglist]
        self.split = [c.parts[-3] for c in self.imglist]
        self.frame = [int(c.parts[-1][0:-(len(c.suffix))]) for c in self.imglist]
        
    def update_labels(self):
        '''loads labels for each frame in imglist'''
        self.update_index()
        chars = pd.unique(self.char)
        sessions = pd.unique(self.session)
        splits = pd.unique(self.split)
        
        label_names = ["char", "session", "split", "frame", "time", "mouse","mouse_x", "mouse_y", "keyboard"]
        self.labels = pd.DataFrame(columns=label_names)  
        for c in chars:
            for ses in sessions:
                for sp in splits:
                    try:
                        loc = Path(self.mainpath, c, str(ses), sp, "Input.csv")
                        data = pd.read_csv(loc)
                        data.columns =  label_names[3:]
                        data["char"] = c
                        data["session"] = ses
                        data["split"] = sp
                        self.labels = self.labels.append(data)
                    except:
                        pass
        
        self.labels = self.labels.set_index(["char", "session", "split", "frame"])
    
    def get_data(self, load_labels=True, sort=True, load_imgs=False, img_size=None, greyscale=False, img_mode="numpy"):
        '''return data as pandas DataFrame'''
        if load_labels:
            self.update_labels()
        else:
            self.update_index()
            
        df = pd.DataFrame({"char":self.char,
            "session":self.session,
            "split":self.split,
            "frame":self.frame,
            "img":self.imglist})

        if load_imgs:
            df["img"] = df["img"].apply(lambda x: Image.open(x))
            
            if img_size is not None:
                df["img"] = df["img"].apply(lambda x: x.resize(img_size))
                
            if greyscale:
                df["img"] = df["img"].apply(lambda x: x.convert(mode="L"))
            
            if img_mode is "numpy":
                df["img"] = df["img"].apply(lambda x: np.array(x))
        
        df = df.set_index(["char", "session", "split", "frame"])
        
        if load_labels:
            df = df.join(self.labels, on=["char", "session", "split", "frame"], how="left")
        
        if sort:
            df = df.sort_values(by=["char", "session", "split", "frame"])
            
        return df
    
    def load_images(self, mode="numpy"):
        '''load all images from imglist'''
        if mode is "numpy":
            return [np.array(Image.open(img)) for img in self.imglist]
        else:
            return [Image.open(img) for img in self.imglist]