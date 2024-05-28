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

from settings.settings import *

class QRSettings(QWidget):
    def __init__(self) -> None:
        super(QRSettings, self).__init__()
        
        self.VBL = QVBoxLayout()
        self.title = QLabel("QR Generation")
        self.title.setStyleSheet("font-size: 24pt; font-weight: bold")
        self.setStyleSheet("""
            .QLabel {
                font-size: 16pt;
                color: white;
                padding-top: 35px;
            }
        """)
        self.setContentsMargins(10, 10, 25, 15)
        self.VBL.setAlignment(Qt.AlignTop)
        
        # qr file selection
        self.qrfileLabel = QLabel("File location")
        self.qrfileSelection = QLineEdit()
        
        # add everything to layout
        self.VBL.addWidget(self.title)
        self.VBL.addWidget(self.qrfileLabel)
        self.VBL.addWidget(self.qrfileSelection)
        self.setLayout(self.VBL)