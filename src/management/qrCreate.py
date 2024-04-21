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

# other libraries
from segno import make_qr
import pyautogui

# Import settings
from settings.settings import all_members

# Constants
width, height = pyautogui.size()

class QRCreateWidget(QWidget):
    def __init__(self) -> None:
        super(QRCreateWidget, self).__init__()
        
        self.VBL = QVBoxLayout()
        self.setStyleSheet("""
            .QLabel {
                font-size: 12pt;
                color: white;
                padding-top: 35px;
            }
        """)
        self.setFixedWidth(int(width*0.4))
        self.setContentsMargins(10, 10, 25, 10)
        self.VBL.setAlignment(Qt.AlignBottom)
        
        # import all identifiers and names
        self.identifiers = all_members.keys()
        self.names = [value[0] for value in all_members.values()]
        
        # identifier combo box
        self.identifier_select = QComboBox()
        self.identifier_select.addItem("ALL")
        self.identifier_select.addItems(self.identifiers)
        self.identifier_select.setEditable(True)
        self.identifier_select.currentIndexChanged.connect(self.SyncOption)
        
        # name combo box
        self.name_select = QComboBox()
        self.name_select.addItem("ALL")
        self.name_select.addItems(self.names)
        self.name_select.setEditable(True)
        self.name_select.currentIndexChanged.connect(self.SyncOption)
        
        # labels for combo boxes
        self.identifier_label = QLabel("Identifier")
        self.name_label = QLabel("Name")
        
        # submit button
        self.SubmitBTN = QPushButton("Submit")
        self.SubmitBTN.clicked.connect(self.Submit)
        
        # thread to create QR codes
        self.Thread1 = QRCreate()
        self.selectionIndex = 0
        
        # add everything to layout
        self.VBL.addWidget(self.identifier_label)
        self.VBL.addWidget(self.identifier_select)
        self.VBL.addWidget(self.name_label)
        self.VBL.addWidget(self.name_select)
        self.VBL.addWidget(self.SubmitBTN)
        self.setLayout(self.VBL)
        
    def SyncOption(self):
        if self.identifier_select.currentIndex() != self.selectionIndex:
            self.selectionIndex = self.identifier_select.currentIndex()
            self.name_select.setCurrentIndex(self.selectionIndex)
        else:
            self.selectionIndex = self.name_select.currentIndex()
            self.identifier_select.setCurrentIndex(self.selectionIndex)
            
    def Submit(self):
        self.Thread1.run(self.selectionIndex)

class QRCreate(QThread):
    def run(self, option: int) -> None:
        if option == 0:
            for identifier, data in all_members.items():
                img = make_qr(identifier)
                img.save(f'./qrcodes/{data[0]}.png',scale=10,border=1)
        else:
            img = make_qr([_ for _ in all_members.keys()][option+1])
            img.save(f'./qrcodes/{[_ for _ in all_members.values()][option-1][0]}.png',scale=10,border=1)
        self.quit()