# -*- coding: utf-8 -*-
"""
Created on Thu May  7 18:37:37 2020

@author: MatelDS
"""

from d2utilities import d2record

minutes = 5
seconds = 0
frameduration = 0.25

char = "assa"
splits = ["den"]

sessionloc = d2record.create_folders(char, splits)

for split in splits:
    err = d2record.record_timed_split(minutes, seconds, sessionloc, frameduration, split)
    
if err:
    print("Error: Session stoped.")
else:
    print(f"Recording completed./n The data was saved in/n {sessionloc}")