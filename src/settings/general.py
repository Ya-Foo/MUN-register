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

from settings.settings import sheets_url, present, cam_id
import cv2, os

class GeneralSettings(QWidget):
    def __init__(self) -> None:
        super(GeneralSettings, self).__init__()
        
        self.VBL = QVBoxLayout()
        
        self.title = QLabel("General")
        self.title.setStyleSheet("font-size: 24pt; font-weight: bold")
        self.setContentsMargins(10, 10, 25, 15)
        self.VBL.setAlignment(Qt.AlignTop)
        
        # camera selection box
        index = 0
        available = []
        i = 10
        while i > 0:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                available.append(index)
                cap.release()
            index += 1
            i -= 1
            os.system('cls||clear')
        
        self.cameraLabel = QLabel("Camera")
        self.cameraSelection = QComboBox()
        self.cameraSelection.addItems(available)
        if str(cam_id) in available:
            self.cameraSelection.setCurrentText(str(cam_id))
        else:
            self.cameraSelection.addItem("Camera unavailable")
            self.cameraSelection.setCurrentText("Camera unavailable")
            
        # sheet url text area
        self.sheeturlLabel = QLabel("Sheet URL")
        self.sheetURLSelection = QLineEdit(sheets_url)
        self.sheetURLSelection.setCursorPosition(0)
        
        # present marker text area
        self.presentmarkerLabel = QLabel("Present marker")
        self.presentmarkerSelection = QLineEdit(present)
                
        # add everything to layout
        self.VBL.addWidget(self.title)
        self.VBL.addWidget(self.cameraLabel)
        self.VBL.addWidget(self.cameraSelection)
        self.VBL.addWidget(self.sheeturlLabel)
        self.VBL.addWidget(self.sheetURLSelection)
        self.VBL.addWidget(self.presentmarkerLabel)
        self.VBL.addWidget(self.presentmarkerSelection)
        self.setLayout(self.VBL)