# -*- coding: utf-8 -*-
"""
Created on Tue May 12 08:04:35 2020

@author: MatelDS
"""

from PyQt5 import QtWidgets, QtCore, uic
import sys

from d2utilities.d2recordsession import d2recordsession

class d2recorderui(QtWidgets.QMainWindow):
    def __init__(self, uipath=None):
        super(d2recorderui, self).__init__() # Call the inherited classes __init__ method
        if uipath is None:
            uic.loadUi('d2recorder_2020-05-15.ui', self) # Load the .ui file
        else:
            uic.loadUi(uipath, self)
        self.show() # Show the GUI
        
        self.session = None
        self.recordingOFF = True
        self.nextsplit = False
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(1)
        
        '''#ui objects
        #PushButtons
        self.btn_add_split = self.findChild(QtWidgets.QPushButton, 'btn_addsplit')
        self.btn_set_split = self.findChild(QtWidgets.QPushButton, 'btn_setsplit')
        self.btn_remove_last_split = self.findChild(QtWidgets.QPushButton, 'btn_removelastsplit')     
        self.btn_next_split = self.findChild(QtWidgets.QPushButton, 'btn_nextsplit')
        self.btn_record_all_splits = self.findChild(QtWidgets.QPushButton, 'btn_recallsplits')
        self.btn_record_timed_split = self.findChild(QtWidgets.QPushButton, 'btn_recordtimed')
        self.btn_stop_all_recordings = self.findChild(QtWidgets.QPushButton, 'btn_stopallrecordings')
        
        #LineEdit Inputs
        self.inp_wndname = self.findChild(QtWidgets.QLineEdit, 'wndname')
        self.inp_dpiaware_xres = self.findChild(QtWidgets.QLineEdit, 'dpiaware_xres')
        self.inp_dpiaware_yres = self.findChild(QtWidgets.QLineEdit, 'dpiaware_yres')
        self.inp_frameduration = self.findChild(QtWidgets.QLineEdit, 'frameduration')
        self.inp_splitname = self.findChild(QtWidgets.QLineEdit, 'splitinput')
        
        #other input elements
        self.inp_dpiaware = self.findChild(QtWidgets.QCheckBox, 'dpiaware_checkBox')
        self.inp_char = self.findChild(QtWidgets.QComboBox, 'char_selection')
        self.inp_recordtime = self.findChild(QtWidgets.QTimeEdit, 'recordtime')
        
        #other output elements
        self.outp_sessionnumber = self.findChild(QtWidgets.QLCDNumber, 'sessionr')
        self.outp_splitlist = self.findChild(QtWidgets.QListWidget, 'splitlist')'''
        
        #button actions
        self.btn_addsplit.clicked.connect(self.add_split)
        self.btn_setsplit.clicked.connect(self.set_split)
        self.btn_removelastsplit.clicked.connect(self.remove_selected_split)
        
        self.btn_recallsplits.clicked.connect(self.record_all_splits)
        self.btn_nextsplit.clicked.connect(self.next_split)
        self.btn_recordtimed.clicked.connect(self.record_timed)
        self.btn_stopallrecordings.clicked.connect(self.stop_recording)
        
    def record_all_splits(self):
        self.make_session()
        splits = [str(self.splitlist.item(i).text()) for i in range(self.splitlist.count())]
        self.session.create_folders(splits=splits, update_session=False)
        split = splits[0]
        self.splitlist.item(0).setSelected(True)
        self.session.start_recording(split=split, new_session=False)
            
    def next_split(self):
        if self.session is not None:
            splits = [str(self.splitlist.item(i).text()) for i in range(self.splitlist.count())]
            if len(splits) <= 1:
                self.stop_recording()
            else:
                split = splits[1]
                self.session.stop_recording()
                self.splitlist.item(0).setSelected(True)
                self.remove_selected_split()
                self.splitlist.item(0).setSelected(True)
                self.session.start_recording(split=split, new_session=False)                                
    
    def record_timed(self):
        self.make_session()
        self.session.add_minutes(self.recordtime.time().minute())
        self.session.add_seconds(self.recordtime.time().second())
        self.set_split(item="timed")
        self.session.start_recording(split="timed", duration=True)
    
    def stop_recording(self):
        try:
            self.session.stop_recording()
            self.set_split(item="None")
        except:
            pass
        
    def make_session(self):
        '''create recording session with inputs from UI'''
        #check for correct inputs
        splits = [str(self.splitlist.item(i).text()) for i in range(self.splitlist.count())]
        if len(splits) == 0:
            self.set_split()
            splits =["None"]
            
        try:
            frameduration = float(self.frameduration.text())
        except:
            frameduration = 0.1
        
        try:
            xres = int(self.dpiaware_xres.text())
            yres = int(self.dpiaware_yres.text())
        except:
            xres, yres = 646, 509
            
        #initialize recordingsession
        try:
            self.session = d2recordsession(char=str(self.char_selection.currentText()),
                                       splits = splits,
                                       frameduration = frameduration,
                                       wndname = self.wndname.text(),
                                       dpiaware = self.dpiaware_checkBox.isChecked(),
                                       dpiaware_wndsize = (xres, yres))
        except:
            pass
        
    def add_split(self):
        if self.splitinput.text() is not None and len(self.splitinput.text())<25:           
            self.splitlist.addItem(self.splitinput.text())
        else:
            self.splitlist.addItem("None")
            
    def set_split(self, item=None):
        self.splitlist.clear()
        if type(item) is str:
            self.splitlist.addItem(item)
        elif self.splitinput.text() is not None and len(self.splitinput.text())<25:           
            self.splitlist.addItem(self.splitinput.text())
        else:
            self.splitlist.addItem("None")
            
    def remove_selected_split(self):
        listItems=self.splitlist.selectedItems()
        if not listItems: return        
        for item in listItems:
           self.splitlist.takeItem(self.splitlist.row(item))
           
    def update_all(self):
        if self.session is not None:
            self.recordingOFF = self.session.stopped()
            self.session_nbr.display(self.session.session_number)
        
        if not self.recordingOFF:      
            self.btn_addsplit.setEnabled(False)
            self.btn_setsplit.setEnabled(False)
            self.btn_removelastsplit.setEnabled(False)           
            self.btn_recallsplits.setEnabled(False)
            self.btn_recordtimed.setEnabled(False)
            
            self.wndname.setEnabled(False)
            self.frameduration.setEnabled(False)
            self.dpiaware_checkBox.setEnabled(False)
            self.dpiaware_xres.setEnabled(False), self.dpiaware_yres.setEnabled(False)
            self.splitinput.setEnabled(False)
            self.char_selection.setEnabled(False)
            self.recordtime.setEnabled(False)
            self.splitlist.setEnabled(False)
            
            self.btn_stopallrecordings.setEnabled(True)
            self.btn_nextsplit.setEnabled(True)
        else:
            self.btn_addsplit.setEnabled(True)
            self.btn_setsplit.setEnabled(True)
            self.btn_removelastsplit.setEnabled(True)           
            self.btn_recallsplits.setEnabled(True)
            self.btn_recordtimed.setEnabled(True)
            
            self.wndname.setEnabled(True)
            self.frameduration.setEnabled(True)
            self.dpiaware_checkBox.setEnabled(True)
            self.dpiaware_xres.setEnabled(True), self.dpiaware_yres.setEnabled(True)
            self.splitinput.setEnabled(True)
            self.char_selection.setEnabled(True)
            self.recordtime.setEnabled(True)
            self.splitlist.setEnabled(True)
            
            self.btn_stopallrecordings.setEnabled(False)
            self.btn_nextsplit.setEnabled(False)
  
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = d2recorderui()
    app.exec_()