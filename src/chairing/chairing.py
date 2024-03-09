# Import PyQT
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pyautogui

from settings.settings import *
from chairing.record import RecordWidget
from chairing.timer import TimerWidget
from chairing.vote import VoteWidget

# Constants
width, height = pyautogui.size()

class Chairing(QWidget):
    def __init__(self) -> None:
        super(Chairing, self).__init__()
        
        self.VBL = QVBoxLayout()
        
        # top frame (speech and vote)
        self.TopFrame = QFrame()
        self.TopFrameLayout = QHBoxLayout()
        
        # top frame split
        self.TopRightFrame = VoteWidget()
        self.TopLeftFrame = RecordWidget()
        
        # add two subframe (top-left, top-right) into the top frame
        self.TopFrameLayout.addWidget(self.TopLeftFrame)
        self.TopFrameLayout.addWidget(self.TopRightFrame)
        self.TopFrame.setLayout(self.TopFrameLayout)
        
        # bottom frame (timer)
        self.BottomFrame = TimerWidget()
        
        # add the two frames inside main VBL
        self.VBL.addWidget(self.TopFrame)
        self.VBL.addWidget(self.BottomFrame)
        self.setLayout(self.VBL)