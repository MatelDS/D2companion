# -*- coding: utf-8 -*-
"""
Created on Thu May  7 18:37:37 2020

@author: MatelDS
"""

from d2utilities.d2session import d2session

minutes = 5
seconds = 0
frameduration = 0.25

char = "assa"
splits = ["den"]

sess = d2session(char=char, splits=splits, frameduration=frameduration, dpiaware=True)

sess.add_minutes(minutes)
sess.add_seconds(seconds)

sess.record_all_splits()