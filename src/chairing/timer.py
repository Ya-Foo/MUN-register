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

class TimerWidget(QWidget):
    def __init__(self) -> None:
        super(TimerWidget, self).__init__()
        
        self.HBL = QHBoxLayout()
        
        #https://www.youtube.com/watch?v=E7lhFwcDpMI
        
        # set the timer
        self.TimerHourSet = QDoubleSpinBox()
        self.TimerHourSet.setDecimals(0)
        self.TimerHourSet.setMaximum(24)
        self.TimerMinuteSet = QDoubleSpinBox()
        self.TimerMinuteSet.setDecimals(0)
        self.TimerMinuteSet.setMaximum(59)
        self.TimerSecondSet = QDoubleSpinBox()
        self.TimerSecondSet.setDecimals(0)
        self.TimerSecondSet.setMaximum(59)
        
        # start/stop/reset btn
        self.StartBTN = QPushButton("Start")
        self.StopBTN = QPushButton("Stop")
        self.ResetBTN = QPushButton("Reset")
        
        # add everything to layout
        self.HBL.addWidget(self.TimerHourSet)
        self.HBL.addWidget(self.TimerMinuteSet)
        self.HBL.addWidget(self.TimerSecondSet)
        self.HBL.addWidget(self.StartBTN)
        self.HBL.addWidget(self.StopBTN)
        self.HBL.addWidget(self.ResetBTN)
        self.setLayout(self.HBL)


class Timer(QThread):
    def __init__(self) -> None:
        super(Timer, self).__init__()
        
    def run() -> None:
        pass