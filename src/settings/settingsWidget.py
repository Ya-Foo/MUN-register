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

import json
from settings.settings import *


class Settings(QWidget):
    def __init__(self) -> None:
        super(Settings, self).__init__()
        
        self.VBL = QVBoxLayout()
        
        # content frame
        self.ContentFrame = QFrame()
        self.ContentFrameLayout = QHBoxLayout()
        self.ContentFrameLayout.setSpacing(0)
        
        # split into two sides
        self.LeftFrame = QFrame()
        self.LeftFrameLayout = QVBoxLayout()
        self.RightFrame = QFrame()
        self.RightFrameLayout = QVBoxLayout()
        
        # add stuff to left side
        
        # add stuff to right side
        
        # scroll area for left side
        self.LeftScroll = QScrollArea()
        self.LeftScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.LeftScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.LeftScroll.setStyleSheet("QScrollBar {width:0px;}")
        self.LeftScroll.setWidgetResizable(True)
        self.LeftScroll.setWidget(self.LeftFrame)
        
        # scroll area for right side
        self.RightScroll = QScrollArea()
        self.RightScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.RightScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.RightScroll.setStyleSheet("QScrollBar {width:0px;}")
        self.RightScroll.setWidgetResizable(True)
        self.RightScroll.setWidget(self.RightFrame)
        
        # add the two sides
        self.ContentFrameLayout.addWidget(self.LeftScroll)
        self.ContentFrameLayout.addWidget(self.RightScroll)
        self.ContentFrame.setLayout(self.ContentFrameLayout)
        
        # save button
        self.SaveBTN = QPushButton("Save")
        self.SaveBTN.clicked.connect(self.save)
        
        # add everything to main
        self.VBL.addWidget(self.ContentFrame)
        self.VBL.addWidget(self.SaveBTN)
        self.setLayout(self.VBL)
        
    def save(self) -> None:
        new_data = data
        with open("src/settings/config.json", 'w') as f:
            json.dump(new_data, f)