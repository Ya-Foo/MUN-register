# Import PyQT
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pyautogui

# Import from Python files
from qrRead import QRRead
from qrCreate import QRCreate

# Constants
width, height = pyautogui.size()

class MainWindow(QWidget):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        
        self.Grid = QGridLayout()
        self.setWindowTitle("MUN Registration")
        
        # top and bottom frames
        self.TopFrame = QFrame()
        self.BottomFrame = QFrame()
        self.BottomFrame.setStyleSheet(".QFrame{background-color: #1d1d1d; border-radius: 20px;} ")
        self.TopFrameGrid = QGridLayout()
        self.BottomFrameGrid = QGridLayout()
        self.TopFrame.setLayout(self.TopFrameGrid)
        self.BottomFrame.setLayout(self.BottomFrameGrid)
        
        # widget to store camera feed
        self.FeedLabel = QLabel()
        self.FeedLabel.setFixedSize(width//5*3, height//2)
        
        # Labels to display scanned info
        self.IdentifierLabel = QLabel("Not detected")
        self.IdentifierLabel.setStyleSheet("font-size: 18pt;")
        self.NameLabel = QLabel("Not detected")
        self.NameLabel.setStyleSheet("font-size: 18pt;")
        
        # Frame to group info labels
        self.InfoBoxFrame = QFrame()
        self.InfoBoxGrid = QGridLayout()
        self.InfoBoxGrid.addWidget(self.IdentifierLabel, 0, 0)
        self.InfoBoxGrid.addWidget(self.NameLabel, 1, 0)
        self.InfoBoxFrame.setLayout(self.InfoBoxGrid)
        
        # Putting things into top frame
        self.TopFrameGrid.addWidget(self.InfoBoxFrame, 0, 1)
        self.TopFrameGrid.addWidget(self.FeedLabel, 0, 0)
        self.Grid.addWidget(self.TopFrame, 0, 0)
        
        # button to create QR codes
        self.QRCreateBTN = QPushButton("Create QR codes")
        self.QRCreateBTN.clicked.connect(self.CreateQR)
        
        # button to open settings
        self.SettingsBTN = QPushButton("Settings")
        
        # Frame to group all buttons
        self.BTNFrame = QFrame()
        self.BTNFrameGrid = QGridLayout()
        self.BTNFrameGrid.addWidget(self.QRCreateBTN, 0, 0)
        self.BTNFrameGrid.addWidget(self.SettingsBTN, 1, 0)
        self.BTNFrame.setLayout(self.BTNFrameGrid)
        
        # Putting things in bottom frame
        self.BottomFrameGrid.addWidget(self.BTNFrame, 0, 0)
        self.Grid.addWidget(self.BottomFrame, 1, 0)
        
        # thread for registration
        self.Thread1 = QRRead()
        self.Thread1.start()
        self.Thread1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.Thread1.InfoUpdate.connect(self.IdentifierUpdateSlot)
        self.Thread1.NameUpdate.connect(self.NameUpdateSlot)
        
        # thread for QR generation
        self.Thread2 = QRCreate()
        
        self.setLayout(self.Grid)
        self.showMaximized()
        
    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))
        
    def IdentifierUpdateSlot(self, Text):
        self.IdentifierLabel.setText(Text)
        
    def NameUpdateSlot(self, Text):
        self.NameLabel.setText(Text)
        
    def CancelFeed(self):
        self.Thread1.stop()
        
    def CreateQR(self):
        self.Thread2.start()

        
if __name__ == "__main__":
    # Main app
    App = QApplication(['-platform', 'windows:darkmode=1'])
    
    # Dark theme
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(18, 18, 18))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.ButtonText, Qt.black)
    App.setPalette(palette)
    App.setStyleSheet(".QPushButton{background-color: #BB86FC}")
    
    Root = MainWindow()
    Root.show()
    App.exec()