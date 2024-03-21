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

from chairing.speech import RecordWidget
from chairing.timer import TimerWidget
from chairing.vote import VoteWidget

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