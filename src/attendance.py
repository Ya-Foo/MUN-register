# Import PyQT
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pyautogui

from qrRead import QRRead

# Constants
width, height = pyautogui.size()

class Attendance(QWidget):
    def __init__(self) -> None:
        super(Attendance, self).__init__()
        
        self.VBL = QVBoxLayout()
        self.VBL.setSpacing(0)
        self.VBL.setContentsMargins(10,10,10,10)
        self.VBL.setAlignment(Qt.AlignHCenter)
        
        # bottom frame to store labels
        self.BottomFrame = QFrame()
        self.BottomFrameGrid = QGridLayout()
        
        # Labels to display scanned info
        self.IdentifierHeading = QLabel("Identifier")
        self.IdentifierHeading.setStyleSheet("font-size: 18pt")
        self.IdentifierLabel = QLabel("Not detected")
        self.IdentifierLabel.setStyleSheet("font-size: 18pt;")
        self.NameHeading = QLabel("Name")
        self.NameHeading.setStyleSheet("font-size: 18pt")
        self.NameLabel = QLabel("Not detected")
        self.NameLabel.setStyleSheet("font-size: 18pt;")
        
        # put display scanned info labels into bottom frame
        self.BottomFrameGrid.addWidget(self.IdentifierHeading, 0, 0)
        self.BottomFrameGrid.addWidget(self.IdentifierLabel, 1, 0)
        self.BottomFrameGrid.addWidget(self.NameHeading, 0, 1)
        self.BottomFrameGrid.addWidget(self.NameLabel, 1, 1)
        self.BottomFrame.setLayout(self.BottomFrameGrid)
        
        # label to store camera feed
        self.FeedLabel = QLabel("CAMERA LOADING...")
        self.FeedLabel.setFixedHeight(height//3*2)
        
        # thread for registration
        self.Thread1 = QRRead()
        self.Thread1.start()
        self.Thread1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.Thread1.InfoUpdate.connect(self.IdentifierUpdateSlot)
        self.Thread1.NameUpdate.connect(self.NameUpdateSlot)
        
        # add everything to the grid
        self.VBL.addWidget(self.FeedLabel)
        self.VBL.addWidget(self.BottomFrame)
        
        self.setLayout(self.VBL)
        self.show()
        
    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))
        
    def IdentifierUpdateSlot(self, Text):
        self.IdentifierLabel.setText(Text)
        
    def NameUpdateSlot(self, Text):
        self.NameLabel.setText(Text)