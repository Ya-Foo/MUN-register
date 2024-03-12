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