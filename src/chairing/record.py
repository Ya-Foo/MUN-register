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
            
            .QFrame {
                background-color: rgba(255, 255, 255, 0.3);
                border: 2px solid white;
                border-radius: 10px;
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
        
        # country combo box
        self.country_select = QComboBox()
        self.country_select.setEditable(True)
        
        # speech type combo box
        self.speech_select = QComboBox()
        self.speech_select.addItems(["Speech", "Amendment", "POI"])
        
        # labels for combo boxes
        self.room_label = QLabel("--ROOM--")
        self.country_label = QLabel("--COUNTRY--")
        self.speech_label = QLabel("--SPEECH TYPE--")
        
        # submit button
        self.SubmitBTN = QPushButton("Submit")
        self.SubmitBTN.clicked.connect(self.Submit)
        
        # status update
        self.StatusBox = QFrame()
        self.StatusBoxLayout = QVBoxLayout()
        self.Status = QLabel("Please fill in all of the info.")
        self.Status.setStyleSheet("font: white; font-size: 10pt;")
        self.StatusBoxLayout.addWidget(self.Status)
        self.Status.setLayout(self.StatusBoxLayout)
        
        # add everything to layout
        self.VBL.addWidget(self.room_label)
        self.VBL.addWidget(self.room_select)
        self.VBL.addWidget(self.country_label)
        self.VBL.addWidget(self.country_select)
        self.VBL.addWidget(self.speech_label)
        self.VBL.addWidget(self.speech_select)
        self.VBL.addWidget(self.Status)
        self.VBL.addWidget(self.SubmitBTN)
        self.setLayout(self.VBL)
        self.show()
        
    def Submit(self):
        self.room = self.room_select.currentIndex()
        self.country = self.country_select.currentText()
        self.speech = self.speech_select.currentText()
        self.submissionThread = self.SelectedRoom[self.room]
        self.submissionThread.run(self.country, self.speech)
        self.submissionThread.ProgressUpdate.connect(self.DisplayProgress)
        
    def ChangeRoom(self):
        self.country_select.clear()
        self.country_select.addItems(self.SelectedRoom[self.room_select.currentIndex()].country_list)
        
    def DisplayProgress(self, done: bool):
        if done:
            self.Status.setStyleSheet("""background-color: green;""")
        else:
            self.Status.setStyleSheet("""background-color: red;""")

class RecordEngagement(QThread):
    # Initialise thread's progress signal
    ProgressUpdate = pyqtSignal(bool)
    
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
            self.ProgressUpdate.emit(1)
            self.quit()
        except:
            self.ProgressUpdate.emit(0)