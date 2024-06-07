"""
MIT License

Copyright (c) 2024 Gia Phu Huynh and Quang Hien Bui

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Import PyQT
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtTest

import time

class TimerWidget(QWidget):
    def __init__(self) -> None:
        super(TimerWidget, self).__init__()
        
        self.HBL = QHBoxLayout()
        
        #https://www.youtube.com/watch?v=E7lhFwcDpMI
        
        # set the timer
        self.timeSet = QLineEdit()
        
        # start/stop btn
        self.StartBTN = QPushButton("Start")
        self.StartBTN.clicked.connect(self.start_timer)
        self.StopBTN = QPushButton("Stop and reset")
        self.StopBTN.clicked.connect(self.stop_timer)
        
        # timer thread
        self.TimerThread = Timer()
        self.TimerThread.TimeSignal.connect(self.displayTime)
        
        # display remaining time
        self.TimeRemaining = QLineEdit("00:00:00")
        self.TimeRemaining.setReadOnly(True)

        # add everything to layout
        self.HBL.addWidget(self.TimeRemaining)
        self.HBL.addWidget(self.timeSet)
        self.HBL.addWidget(self.StartBTN)
        self.HBL.addWidget(self.StopBTN)
        self.setLayout(self.HBL)
    
    def start_timer(self) -> None:
        hours, minutes, seconds = 0, 0, 0
        self.timeEntry = self.timeSet.text().split(":")
        try:
            if len(self.timeEntry) == 3:
                hours = int(self.timeEntry[0])
                minutes = int(self.timeEntry[1])
                seconds = int(self.timeEntry[2])
            elif len(self.timeEntry) == 2:
                minutes = int(self.timeEntry[0])
                seconds = int(self.timeEntry[1])
            elif len(self.timeEntry) == 1:
                seconds = int(self.timeEntry[0])
            else:
                self.TimeRemaining.setText("Invalid time format")
                return
        except ValueError:
            self.TimeRemaining.setText("Invalid time format")
            return
        
        self.TimerThread.run(hours, minutes, seconds)
        
    def displayTime(self, time: str):
        self.TimeRemaining.setText(time)
        
    def stop_timer(self):
        self.TimerThread.stop()

class Timer(QThread):
    # Initialise thread's signal
    TimeSignal = pyqtSignal(str)
        
    def run(self, hours: int, minutes: int, seconds: int) -> None:
        self.stopTimer = False
        totalSeconds = (hours*3600) + (minutes * 60) + seconds
        while totalSeconds > 0 and not self.stopTimer:
            minutes, seconds = divmod(totalSeconds, 60)
            hours, minutes = divmod(minutes, 60)
            
            formated_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.TimeSignal.emit(formated_time)
            
            QtTest.QTest.qWait(1000)
            totalSeconds -= 1
            
        if not self.stopTimer:
            self.TimeSignal.emit("Time's up!")
        else:
            self.TimeSignal.emit("00:00:00")
        self.quit()
            
    def stop(self) -> None:
        self.stopTimer = True
        self.quit()