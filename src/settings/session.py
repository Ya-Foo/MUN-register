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

from settings.settings import attendance_lookup_col, attendance_register_col, amendment_col, country_col, poi_col, speech_col

class SessionSettings(QWidget):
    def __init__(self) -> None:
        super(SessionSettings, self).__init__()
        
        self.VBL = QVBoxLayout()
        self.title = QLabel("Session")
        self.title.setStyleSheet("font-size: 24pt; font-weight: bold")
        self.setContentsMargins(10, 10, 25, 15)
        self.VBL.setAlignment(Qt.AlignTop)
        
        # page selection box
        self.pageLabel = QLabel("Page")
        self.pageSelection = QComboBox()
        
        # start row counter
        self.startrowLabel = QLabel("Start row")
        self.startrowCounter = QDoubleSpinBox()
        
        # identifier text area
        self.identifierLabel = QLabel("Identifier Column")
        self.identifierSelection = QLineEdit(attendance_lookup_col)
        
        # country text area
        self.countryLabel = QLabel("Country Column")
        self.countrySelection = QLineEdit(country_col)
        
        # attendance text area
        self.registerLabel = QLabel("Register Column")
        self.registerSelection = QLineEdit(attendance_register_col)
        
        # speech text area
        self.speechLabel = QLabel("Speech Column")
        self.speechSelection = QLineEdit(speech_col)
        
        # amendment text area
        self.amendmentLabel = QLabel("Amendment Column")
        self.amendmentSelection = QLineEdit(amendment_col)
        
        # poi text area
        self.poiLabel = QLabel("POI Column")
        self.poiSelection = QLineEdit(poi_col)
        
        # add everything to layout
        self.VBL.addWidget(self.title)
        self.VBL.addWidget(self.pageLabel)
        self.VBL.addWidget(self.pageSelection)
        self.VBL.addWidget(self.startrowLabel)
        self.VBL.addWidget(self.startrowCounter)
        self.VBL.addWidget(self.identifierLabel)
        self.VBL.addWidget(self.identifierSelection)
        self.VBL.addWidget(self.countryLabel)
        self.VBL.addWidget(self.countrySelection)
        self.VBL.addWidget(self.registerLabel)
        self.VBL.addWidget(self.registerSelection)
        self.VBL.addWidget(self.speechLabel)
        self.VBL.addWidget(self.speechSelection)
        self.VBL.addWidget(self.amendmentLabel)
        self.VBL.addWidget(self.amendmentSelection)
        self.VBL.addWidget(self.poiLabel)
        self.VBL.addWidget(self.poiSelection)
        self.setLayout(self.VBL)