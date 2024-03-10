# Import PyQT
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from settings.settings import *
import api

class RecordWidget(QWidget):
    def __init__(self) -> None:
        super(RecordWidget, self).__init__()
        
        self.VBL = QVBoxLayout()
        self.VBL.setAlignment(Qt.AlignTop)
        self.setStyleSheet("""
            .QComboBox {
                border: 1px solid transparent;
                border-radius: 10px;
                background: #272727;
                color: #6b6b6b;
                padding-top: 10px;
                padding-bottom: 10px;
                padding-left: 10px;
                font-size: 10pt;
            }
            .QComboBox::drop-down {
                border: 1px solid;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
                background: #222222;
                padding-right: 5px;
                padding-left: 5px;
            }
        
            .QPushButton {
                background-color: #3A668B;
                font: black;
            }
            .QPushButton:hover {
                background-color: #172A41;
            }
        """)
        
        # create each room class
        self.SelectedRoom = []
        for room in attendance_rooms:
            self.SelectedRoom.append(RecordEngagement(room))
            
        # room combo box
        self.room_select = QComboBox()
        self.room_select.addItems(attendance_rooms)
        self.room_select.currentTextChanged.connect(self.ChangeRoom)
        
        # speech type combo box
        self.speech_select = QComboBox()
        self.speech_select.addItems(["Speech", "Amendment", "POI"])
        
        # country combo box
        self.country_select = QComboBox()
        self.country_select.addItems(self.SelectedRoom[self.room_select.currentIndex()].country_list)
        self.country_select.setEditable(True)
        
        # labels for combo boxes
        self.room_label = QLabel("--ROOM--")
        self.speech_label = QLabel("--SPEECH TYPE--")
        self.country_label = QLabel("--COUNTRY--")
        
        # submit button
        self.SubmitBTN = QPushButton("Submit")
        self.SubmitBTN.clicked.connect(self.Submit)
        
        # add everything to layout
        self.VBL.addWidget(self.room_label)
        self.VBL.addWidget(self.room_select)
        self.VBL.addWidget(self.speech_label)
        self.VBL.addWidget(self.speech_select)
        self.VBL.addWidget(self.country_label)
        self.VBL.addWidget(self.country_select)
        self.VBL.addWidget(self.SubmitBTN)
        self.setLayout(self.VBL)
        self.show()
        
    def Submit(self):
        self.room = self.room_select.currentIndex()
        self.country = self.country_select.currentText()
        self.speech = self.speech_select.currentText()
        self.submissionThread = self.SelectedRoom[self.room]
        self.submissionThread.run(self.country, self.speech)
        
    def ChangeRoom(self):
        self.country_select.clear()
        self.country_select.addItems(self.SelectedRoom[self.room_select.currentIndex()].country_list)

class RecordEngagement(QThread):    
    def __init__(self, room: str) -> None:
        super(RecordEngagement, self).__init__()
        self.room = room
        
        self.country_cells = f"'{self.room}'!{country_col}{attendance_start}:{country_col}1000"
        self.country_list = [i[0] for i in api.get_values(creds, sheets_id, self.country_cells)]
        
    def run(self, country: str, speechType: str) -> None:
        try:
            match speechType:
                case "Speech":
                    self.write_col = speech_col
                case "Amendment":
                    self.write_col = amendment_col
                case "POI":
                    self.write_col = poi_col
            self.write_cell = f"'{self.room}'!{self.write_col}{self.country_list.index(country)+attendance_start}"
            
            # check if box empty: if yes, just add; otherwise concatenate another '/'
            self.current = api.get_values(creds, sheets_id, self.write_cell)
            self.write_content = present
            if len(self.current) > 0:
                self.write_content = self.current[0][0] + present
                
            api.write_values(creds, sheets_id, self.write_cell, 'USER_ENTERED', self.write_content)
            self.quit()
        except:
            pass