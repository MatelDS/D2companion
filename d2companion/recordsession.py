# -*- coding: utf-8 -*-
"""
Created on Thu May  7 18:37:37 2020

@author: MatelDS
"""

from PyQt5 import QtWidgets
import sys

from gui.d2recordergui import d2recorderui

uipath = ".//gui//d2recorder_2020-05-15.ui"
app = QtWidgets.QApplication(sys.argv)
recordui_wnd = d2recorderui(uipath=uipath)
app.exec_()