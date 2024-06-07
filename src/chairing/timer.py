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

import pyautogui

# Constants
width, height = pyautogui.size()

class TimerWidget(QWidget):
    def __init__(self) -> None:
        super(TimerWidget, self).__init__()
        
        self.HBL = QHBoxLayout()
        self.setContentsMargins(10, 10, 25, 15)
        
        #https://www.youtube.com/watch?v=E7lhFwcDpMI
        
        # right frame for timer controls
        self.RightFrame = QFrame()
        self.RightFrameLayout = QVBoxLayout()
        self.RightBottomFrame = QFrame()
        self.RightBottomFrameLayout = QHBoxLayout()
        
        # set the timer
        self.timeSet = QLineEdit()
        self.timeSet.setStyleSheet("""
            color: #6f6f6f;
            border: 2px solid white;
            border-radius: 10;
            background: transparent;
            font-size: 32pt;
        """)
        
        # start, stop, clear, reset btn
        self.StartBTN = QPushButton("Start")
        self.StartBTN.clicked.connect(self.start_timer)
        self.StopBTN = QPushButton("Stop")
        self.StopBTN.clicked.connect(self.stop_timer)
        self.ResetBTN = QPushButton("Reset")
        self.ResetBTN.clicked.connect(self.reset_timer)
        self.ClearBTN = QPushButton("Clear")
        self.ClearBTN.clicked.connect(self.clear_timer)
        
        # add stuff to right frame
        self.RightBottomFrameLayout.addWidget(self.StartBTN)
        self.RightBottomFrameLayout.addWidget(self.StopBTN)
        self.RightBottomFrameLayout.addWidget(self.ResetBTN)
        self.RightBottomFrameLayout.addWidget(self.ClearBTN)
        self.RightBottomFrame.setLayout(self.RightBottomFrameLayout)
        self.RightFrameLayout.addWidget(self.timeSet)
        self.RightFrameLayout.addWidget(self.RightBottomFrame)
        self.RightFrame.setLayout(self.RightFrameLayout)
        self.RightFrame.setFixedWidth(width//3)
        self.RightFrameLayout.setAlignment(Qt.AlignTop)
        
        # timer thread
        self.TimerThread = Timer()
        self.TimerThread.TimeSignal.connect(self.displayTime)
        
        # display remaining time
        self.TimeRemaining = QLabel("00:00:00")
        self.TimeRemaining.setStyleSheet("""
            color: white;
            font-size: 112pt;
        """)
        self.TimeRemaining.setAlignment(Qt.AlignCenter)

        # add everything to layout
        self.HBL.addWidget(self.TimeRemaining)
        self.HBL.addWidget(self.RightFrame)
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
                return
        except ValueError:
            return
        
        minutes += seconds // 60
        seconds %= 60
        hours += minutes // 60
        minutes %= 60
        if hours > 24:
            return
        self.TimerThread.run(hours, minutes, seconds)
        
    def displayTime(self, time: str):
        self.TimeRemaining.setText(time)
        
    def stop_timer(self):
        self.TimerThread.stop()
        
    def reset_timer(self):
        self.TimeRemaining.setText(self.TimerThread.history)
        self.timeSet.setText(self.TimerThread.history)
        self.TimerThread.stop()
        
    def clear_timer(self):
        self.TimerThread.stop()
        self.TimeRemaining.setText("00:00:00")
        self.timeSet.setText("")

class Timer(QThread):
    # Initialise thread's signal
    TimeSignal = pyqtSignal(str)
    
    def __init__(self) -> None:
        super(Timer, self).__init__()
        self.totalSeconds = 0
        self.history = "00:00:00"
        
    def run(self, hours: int, minutes: int, seconds: int) -> None:
        self.stopTimer = False
        self.history = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.totalSeconds = (hours*3600) + (minutes * 60) + seconds
        while self.totalSeconds > 0 and not self.stopTimer:
            minutes, seconds = divmod(self.totalSeconds, 60)
            hours, minutes = divmod(minutes, 60)
            
            formated_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.TimeSignal.emit(formated_time)
            
            QtTest.QTest.qWait(1000)
            self.totalSeconds -= 1
        self.quit()
            
    def stop(self) -> None:
        self.stopTimer = True
        self.quit()