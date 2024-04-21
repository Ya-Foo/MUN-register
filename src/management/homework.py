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
import pyautogui

# Import settings
from settings.settings import *

# Constants
width, height = pyautogui.size()

class HomeworkWidget(QWidget):
    def __init__(self) -> None:
        super(HomeworkWidget, self).__init__()
        
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
        self.VBL.setAlignment(Qt.AlignTop)
        
        # identifier combobox
        self.name_select = QComboBox()
        self.name_range = f"'{management_page}'!{management_name_col}{management_start_row}:{management_name_col}1000"
        self.name_list = [i[0] for i in api.get_values(creds, sheets_id, self.name_range)]
        self.name_select.addItems(self.name_list)
        
        # HW category combobox
        self.homework_select = QComboBox()
        self.homework_select.addItems(["Research", "Speech and clauses"])
        
        # status combobox
        self.status_select = QComboBox()
        self.status_select.addItems(management_status)
        
        # labels for combobox
        self.name_label = QLabel("Name")
        self.homework_label = QLabel("Homework category")
        self.status_label = QLabel("Status")
        
        # thread for recording hw
        self.Thread1 = RecordHomework(self.name_list)
        
        # submit button
        self.SubmitBTN = QPushButton("Submit")
        self.SubmitBTN.clicked.connect(self.Submit)
        
        # add everything to main layout
        self.VBL.addWidget(self.name_label)
        self.VBL.addWidget(self.name_select)
        self.VBL.addWidget(self.homework_label)
        self.VBL.addWidget(self.homework_select)
        self.VBL.addWidget(self.status_label)
        self.VBL.addWidget(self.status_select)
        self.VBL.addWidget(self.SubmitBTN)
        self.setLayout(self.VBL)
        
    def Submit(self):
        self.Thread1.run(self.name_select.currentText(), self.homework_select.currentText(), self.status_select.currentText())
        
class RecordHomework(QThread):
    def __init__(self, name_list: list) -> None:
        super(RecordHomework, self).__init__()
        
        self.name_list = name_list
        
    def run(self, name: str, homework: str, status: str) -> None:
        match homework:
            case "Research":
                self.write_col = management_research_col
            case "Speech and clauses":
                self.write_col = management_speech_col
        self.write_cell = f"'{management_page}'!{self.write_col}{self.name_list.index(name)+management_start_row}"
        
        api.write_values(creds, sheets_id, self.write_cell, 'USER_ENTERED', status)
        self.quit()