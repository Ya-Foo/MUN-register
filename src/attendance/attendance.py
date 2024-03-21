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

import pyautogui

from attendance.qrRead import QRRead

# Constants
width, height = pyautogui.size()

class Attendance(QWidget):
    def __init__(self) -> None:
        super(Attendance, self).__init__()
        
        self.VBL = QVBoxLayout()
        self.VBL.setSpacing(0)
        self.VBL.setContentsMargins(10,10,10,10)
        self.VBL.setAlignment(Qt.AlignHCenter)
        self.setStyleSheet(".QLabel{font: 18pt;}")
        
        # bottom frame to store labels
        self.BottomFrame = QFrame()
        self.BottomFrameLayout = QHBoxLayout()
        
        # top frame for cam and wojaks
        self.TopFrame = QFrame()
        self.TopFrameLayout = QStackedLayout()
        
        # identifer and name frames
        self.InfoFrameStyle = ".QFrame{border: 5px solid #3f5a88; border-radius:40px; margin: 25px;}"
        self.IdentifierFrame = QFrame()
        self.IdentifierFrame.setStyleSheet(self.InfoFrameStyle)
        self.IdentifierFrameLayout = QVBoxLayout()
        self.NameFrame = QFrame()
        self.NameFrame.setStyleSheet(self.InfoFrameStyle)
        self.NameFrameLayout = QVBoxLayout()
        
        # Labels to display scanned info
        self.IdentifierHeading = QLabel("IDENTIFIER")
        self.IdentifierHeading.setAlignment(Qt.AlignCenter)
        self.IdentifierLabel = QLabel("Not detected")
        self.IdentifierLabel.setAlignment(Qt.AlignCenter)
        self.NameHeading = QLabel("NAME")
        self.NameHeading.setAlignment(Qt.AlignCenter)
        self.NameLabel = QLabel("Not detected")
        self.NameLabel.setAlignment(Qt.AlignCenter)
        
        # add labels into identifier and name frame
        self.IdentifierFrameLayout.addWidget(self.IdentifierHeading)
        self.IdentifierFrameLayout.addWidget(self.IdentifierLabel)
        self.IdentifierFrame.setLayout(self.IdentifierFrameLayout)
        
        self.NameFrameLayout.addWidget(self.NameHeading)
        self.NameFrameLayout.addWidget(self.NameLabel)
        self.NameFrame.setLayout(self.NameFrameLayout)
        
        # put display scanned info frames into bottom frame
        self.BottomFrameLayout.addWidget(self.IdentifierFrame)
        self.BottomFrameLayout.addWidget(self.NameFrame)
        self.BottomFrame.setLayout(self.BottomFrameLayout)
        
        # label to store camera feed
        self.FeedLabel = QLabel("CAMERA LOADING...")
        self.FeedLabel.setFixedSize(width//5*4, height//3*2)
        
        # label for wojaks
        self.Wojaks = QLabel()
        self.WojakGeometry = self.FeedLabel.size()
        self.Wojaks.setPixmap(QPixmap("./icons/sacred_wojaks.png").scaled(self.WojakGeometry))
        self.Wojaks.setFixedSize(self.WojakGeometry)
        
        # thread for registration
        self.Thread1 = QRRead()
        self.Thread1.start()
        self.Thread1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.Thread1.InfoUpdate.connect(self.IdentifierUpdateSlot)
        self.Thread1.NameUpdate.connect(self.NameUpdateSlot)
        
        # add stuff to top frame
        self.TopFrameLayout.addWidget(self.FeedLabel)
        self.TopFrameLayout.addWidget(self.Wojaks)
        self.TopFrameLayout.setStackingMode(QStackedLayout.StackAll)
        self.TopFrame.setLayout(self.TopFrameLayout)
        self.TopFrame.setFixedHeight(height//3*2)
        
        # add everything to the grid
        self.VBL.addWidget(self.TopFrame)
        self.VBL.addWidget(self.BottomFrame)
        self.setLayout(self.VBL)
        
        self.show()
        
    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))
        
    def IdentifierUpdateSlot(self, Text):
        self.IdentifierLabel.setText(Text)
        
    def NameUpdateSlot(self, Text):
        self.NameLabel.setText(Text)