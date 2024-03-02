# Import PyQT
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pyautogui

from settings.settings import *
import api

# Constants
width, height = pyautogui.size()

class Chairing(QWidget):
    def __init__(self) -> None:
        super(Chairing, self).__init__()
        
        self.VBL = QVBoxLayout()
        
        # create each room class
        self.SelectedRoom = []
        for room in attendance_rooms:
            self.SelectedRoom.append(RecordEngagement(room))
        
        # top frame (speech and vote)
        self.TopFrame = QFrame()
        self.TopFrameLayout = QHBoxLayout()
        
        # top frame split
        self.TopRightFrame = QFrame()
        self.TopRightFrameLayout = QVBoxLayout()
        self.TopLeftFrame = QFrame()
        self.TopLeftFrameLayout = QVBoxLayout()
        
        # room combo box
        self.room_select = QComboBox()
        self.room_select.addItems(attendance_rooms)
        
        # country combo box
        self.country_select = QComboBox()
        self.country_select.addItems(self.SelectedRoom[0].country_list)
        
        # speech type combo box
        self.speech_select = QComboBox()
        self.speech_select.addItems(["Speech", "Amendment", "POI"])
        
        # submit button
        self.SubmitBTN = QPushButton("Submit")
        
        # add everything to top left frame (speech)
        self.TopLeftFrameLayout.addWidget(self.room_select)
        self.TopLeftFrameLayout.addWidget(self.country_select)
        self.TopLeftFrameLayout.addWidget(self.speech_select)
        self.TopLeftFrameLayout.addWidget(self.SubmitBTN)
        self.TopLeftFrame.setLayout(self.TopLeftFrameLayout)
        self.TopLeftFrame.setStyleSheet("""
            background-color: white;
        """)
        
        # majority type btn
        self.majorityGroup = QButtonGroup(self.TopRightFrame)
        self.SimpleMajorityBTN = QRadioButton("Simple Majority")
        self.QualifiedMajorityBTN = QRadioButton("Qualified Majority")
        self.majorityGroup.addButton(self.SimpleMajorityBTN)
        self.majorityGroup.addButton(self.QualifiedMajorityBTN)
        
        # for, against, abstain btns
        self.ForBTN = QPushButton
        
        # add everything to top right frame (vote count)
        self.TopRightFrameLayout.addWidget(self.SimpleMajorityBTN)
        self.TopRightFrameLayout.addWidget(self.QualifiedMajorityBTN)
        self.TopRightFrame.setLayout(self.TopRightFrameLayout)
        
        # add two subframe (top-left, top-right) into the top frame
        self.TopFrameLayout.addWidget(self.TopLeftFrame)
        self.TopFrameLayout.addWidget(self.TopRightFrame)
        self.TopFrame.setLayout(self.TopFrameLayout)
        
        # bottom frame (timer)
        self.BottomFrame = QFrame()
        self.BottomFrameLayout = QHBoxLayout()
        
        # set the timer
        self.TimerHourSet = QDoubleSpinBox()
        self.TimerHourSet.setDecimals(0)
        self.TimerHourSet.setMaximum(24)
        self.TimerMinuteSet = QDoubleSpinBox()
        self.TimerMinuteSet.setDecimals(0)
        self.TimerMinuteSet.setMaximum(59)
        self.TimerSecondSet = QDoubleSpinBox()
        self.TimerSecondSet.setDecimals(0)
        self.TimerSecondSet.setMaximum(59)
        
        # add everything to bottom frame
        self.BottomFrameLayout.addWidget(self.TimerHourSet)
        self.BottomFrameLayout.addWidget(self.TimerMinuteSet)
        self.BottomFrameLayout.addWidget(self.TimerSecondSet)
        self.BottomFrame.setLayout(self.BottomFrameLayout)
        
        # add the two frames inside main VBL
        self.VBL.addWidget(self.TopFrame)
        self.VBL.addWidget(self.BottomFrame)
        self.setLayout(self.VBL)
        
        
class RecordEngagement(QThread):
    def __init__(self, room: str) -> None:
        super(RecordEngagement, self).__init__()
        self.room = room
        
        self.country_cells = f"'{self.room}'!{country_col}{attendance_start}:{country_col}1000"
        self.country_list = [i[0] for i in api.get_values(creds, sheets_id, self.country_cells)]
        
    def run(self, country: str, speechType: str) -> None:
        match speechType:
            case "Speech":
                self.write_col = speech_col
            case "Amendment":
                self.write_col = amendment_col
            case "POI":
                self.write_col = poi_col
        self.write_cell = f"'{self.room}'!{self.write_col}{self.country_list.index(country)+attendance_start}"
        self.current = api.get_values(creds, sheets_id, self.write_cell)
        self.write_content = present
        if len(self.current) > 0:
            self.write_content = self.current + present
        api.write_values(creds, sheets_id, self.write_cell, 'USER_ENTERED', self.write_content)