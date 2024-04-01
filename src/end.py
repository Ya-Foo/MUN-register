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

import sys, json

from PyQt5.QtWidgets import QWidget

class ExitWindow(QWidget):
    def __init__(self) -> None:
        super(ExitWindow, self).__init__()
        
        self.setWindowTitle("Exit session")
        self.setWindowIcon(QIcon("./images/logo/black.png"))
        
        self.VBL = QVBoxLayout()
        self.VBL.setContentsMargins(50, 50, 50, 50)
        self.setStyleSheet("""
            .QLabel {margin-bottom:30px;}
            .QPushButton {
                color: #aaaaaa;
                font-size: 12pt;
                border-radius: 10px;
                padding: 20px 0;
            }
            .QPushButton:hover {
                color: white;
            }
        """)
        self.VBL.setAlignment(Qt.AlignCenter)
        
        self.message = QLabel("Would you like to end this session?")
        self.message.setStyleSheet("font:14pt;")
        self.instruction = QLabel("Yes: next session's settings will be created.\n\n"
                                  "No: this session's settings will be kept.")
        self.instruction.setStyleSheet("font:10pt;margin: 0px 20px;")
        
        # frame for btn
        self.BTNFrame = QFrame()
        self.BTNLayout = QHBoxLayout()
        
        # creating buttons
        self.yesBTN = QPushButton("Yes")
        self.yesBTN.setStyleSheet("""
            .QPushButton {background: green}
            .QPushButton:hover {background: #80fa93}
        """)
        self.noBTN = QPushButton("No")
        self.noBTN.setStyleSheet("""
            .QPushButton {background: red}
            .QPushButton:hover {background: #ff7f7f}
        """)
        self.yesBTN.clicked.connect(self.yes)
        self.noBTN.clicked.connect(self.no)
        
        # add everything
        self.BTNLayout.addWidget(self.yesBTN)
        self.BTNLayout.addWidget(self.noBTN)
        self.BTNFrame.setLayout(self.BTNLayout)
        self.VBL.addWidget(self.message)
        self.VBL.addWidget(self.instruction)
        self.VBL.addWidget(self.BTNFrame)
        self.setLayout(self.VBL)
        
        self.show()
        
    def yes(self):
        with open("src/settings/config.json", 'r') as f:
            data = json.loads(f.read())
            session_info = data["session"]
            session_info["register_column"] = increaseCol(session_info["register_column"])
            session_info["amendment_column"] = increaseCol(session_info["amendment_column"])
            session_info["speech_column"] = increaseCol(session_info["speech_column"])
            session_info["poi_column"] = increaseCol(session_info["poi_column"])
        
        with open("src/settings/config.json", 'w') as f:
            f.write(json.dumps(data, indent=4))
        self.close()
    
    def no(self):
        self.close()
        

def increaseCol(x: str) -> str:
    order = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(order)
    new_x = []
    
    # convert into int then +1
    num = 0
    for char in x:
        num *= base
        num += order.index(char) + 1
    num += 1
    
    # convert back to letters
    while num != 0:
        new_x.insert(0, order[num%base-1])
        num //= base
    
    return "".join(new_x)