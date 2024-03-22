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

# Import utility widgets
from management.qrCreate import QRCreateWidget
from management.homework import HomeworkWidget
from management.wiki import WikiWidget

class Managing(QWidget):
    def __init__(self) -> None:
        super(Managing, self).__init__()
        
        self.HBL = QHBoxLayout()
        
        # left frame (qr create and research)
        self.LeftFrame = QFrame()
        self.LeftFrameLayout = QVBoxLayout()
        
        # left frame split
        self.LeftTopFrame = HomeworkWidget()
        self.LeftBottomFrame = QRCreateWidget()
        
        # add two subframes (left-top, left-bottom) into left frame
        self.LeftFrameLayout.addWidget(self.LeftTopFrame)
        self.LeftFrameLayout.addWidget(self.LeftBottomFrame)
        self.LeftFrame.setLayout(self.LeftFrameLayout)
        
        # right frame (wikipedia)
        self.RightFrame = WikiWidget()
        self.RightFrameLayout = QVBoxLayout()
        
        # add stuff into right frame
        self.RightFrame.setLayout(self.RightFrameLayout)
        
        # add two frames inside main HBL
        self.HBL.addWidget(self.LeftFrame)
        self.HBL.addWidget(self.RightFrame)
        self.setLayout(self.HBL)