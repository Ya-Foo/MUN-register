# Import PyQT
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pyautogui, sys

# Import from Python files
from attendance.attendance import Attendance
from chairing.chairing import Chairing

# Constants
width, height = pyautogui.size()

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        
        self.setGeometry(0, 0, width, height)
        self.setWindowTitle("MUN App")
        self.setWindowIcon(QIcon("./icons/logo/black.png"))
        
        # setting up grid to put display
        self.Grid = QGridLayout()
        self.Grid.setContentsMargins(0, 0, 0, 0)
        self.Grid.setSpacing(0)
        
        # central widget
        self.CentralWidget = QWidget()
        self.CentralWidget.setLayout(self.Grid)
        
        # menu
        self.SideMenu = QFrame()
        self.SideMenu.setStyleSheet("""
            .QFrame{background-color: #1d1d1d} 
            .QPushButton{
                text-align:left;
                background-color: transparent;
                font-size: 14pt;
                padding-top: 40px;
                padding-bottom: 40px;
                padding-left: 35px;
                color: #6b6b6b;
                border-radius: 10px;
            }
            .QPushButton:hover{
                background-color: #242424;
                color: #AAAAAA;
                
            }
            .QPushButton:checked{
                background-color: #1976D2;
                color: white;
            }
        """)
        self.SideMenu.setFixedWidth(width//5)
        self.MenuLayout = QVBoxLayout()
        self.MenuLayout.setSpacing(20)
        self.MenuLayout.setContentsMargins(20, 20, 20, 20)
        
        # btn frame
        self.BTNFrame = QFrame()
        self.BTNFrameLayout = QVBoxLayout()
        self.BTNFrameLayout.setAlignment(Qt.AlignTop)
        
        # buttons in menu
        self.AttendanceBTN = QPushButton(" Attendance")
        self.AttendanceBTN.setAutoExclusive(True)
        self.AttendanceBTN.setCheckable(True)
        self.AttendanceICO = QIcon()
        self.AttendanceICO.addPixmap(QPixmap('./icons/checked-user-selected.ico'), QIcon.Normal, QIcon.On)
        self.AttendanceICO.addPixmap(QPixmap('./icons/checked-user.ico'), QIcon.Normal, QIcon.Off)
        self.AttendanceBTN.setIcon(self.AttendanceICO)
        self.AttendanceBTN.setIconSize(QSize(48, 48))
        self.AttendanceBTN.setChecked(1)
        self.AttendanceBTN.clicked.connect(self.AttendanceActivate)
        
        self.ChairingBTN = QPushButton(" Chairing")
        self.ChairingBTN.setAutoExclusive(True)
        self.ChairingBTN.setCheckable(True)
        self.ChairingICO = QIcon()
        self.ChairingICO.addPixmap(QPixmap('./icons/gavel-selected.ico'), QIcon.Normal, QIcon.On)
        self.ChairingICO.addPixmap(QPixmap('./icons/gavel.ico'), QIcon.Normal, QIcon.Off)
        self.ChairingBTN.setIcon(self.ChairingICO)
        self.ChairingBTN.setIconSize(QSize(48, 48))
        self.ChairingBTN.clicked.connect(self.ChairingActivate)
        
        self.ManagementBTN = QPushButton(" Management")
        self.ManagementBTN.setAutoExclusive(True)
        self.ManagementBTN.setCheckable(True)
        self.ManagementICO = QIcon()
        self.ManagementICO.addPixmap(QPixmap('./icons/edit-selected.ico'), QIcon.Normal, QIcon.On)
        self.ManagementICO.addPixmap(QPixmap('./icons/edit.ico'), QIcon.Normal, QIcon.Off)
        self.ManagementBTN.setIcon(self.ManagementICO)
        self.ManagementBTN.setIconSize(QSize(48, 48))
        self.ManagementBTN.clicked.connect(self.ManagingActivate)
        
        self.SettingsBTN = QPushButton(" Settings")
        self.SettingsBTN.setAutoExclusive(True)
        self.SettingsBTN.setCheckable(True)
        self.SettingsICO = QIcon()
        self.SettingsICO.addPixmap(QPixmap('./icons/gear-selected.ico'), QIcon.Normal, QIcon.On)
        self.SettingsICO.addPixmap(QPixmap('./icons/gear.ico'), QIcon.Normal, QIcon.Off)
        self.SettingsBTN.setIcon(self.SettingsICO)
        self.SettingsBTN.setIconSize(QSize(48, 48))
        self.SettingsBTN.clicked.connect(self.SettingsActivate)
        
        # add buttons to menu
        self.BTNFrameLayout.addWidget(self.AttendanceBTN)
        self.BTNFrameLayout.addWidget(self.ChairingBTN)
        self.BTNFrameLayout.addWidget(self.ManagementBTN)
        self.BTNFrameLayout.addWidget(self.SettingsBTN)
        self.BTNFrame.setLayout(self.BTNFrameLayout)
        
        # Copyright frame
        self.copyrightFrame = QFrame()
        self.copyrightFrame.setStyleSheet(".QLabel{font: 8pt; color: rgba(255, 255, 255, 0.25)}")
        self.copyrightFrameLayout = QFormLayout()
        self.logoLabel = QLabel()
        self.logoLabel.setPixmap(QPixmap("./icons/logo/white.png").scaledToWidth(96))
        self.copyrightFrameLayout.addRow(self.logoLabel, QLabel("MIT License\n\nCopyright (c) 2024 Gia Phu Huynh"))
        self.copyrightFrameLayout.setFormAlignment(Qt.AlignBottom)
        self.copyrightFrameLayout.setHorizontalSpacing(25)
        self.copyrightFrame.setLayout(self.copyrightFrameLayout)
        
        # Add everything to side menu
        self.MenuLayout.addWidget(self.BTNFrame)
        self.MenuLayout.addWidget(self.copyrightFrame)
        self.SideMenu.setLayout(self.MenuLayout)
        
        # area for main contents
        self.MainContent = QStackedWidget()
        
        # add 4 tabs: Attendance, Settings, Management, Chairing
        self.Attendance = Attendance()
        self.Managing = QWidget()
        self.Chairing = Chairing()
        self.Settings = QWidget()
        self.MainContent.addWidget(self.Attendance)
        self.MainContent.addWidget(self.Chairing)
        self.MainContent.addWidget(self.Managing)
        self.MainContent.addWidget(self.Settings)
        
        # adding all to main application
        self.Grid.addWidget(self.SideMenu, 0, 0)
        self.Grid.addWidget(self.MainContent, 0, 1)
        
        self.setCentralWidget(self.CentralWidget)
        
        self.showMaximized()
    
    def AttendanceActivate(self):
        self.MainContent.setCurrentIndex(0)
        
    def ChairingActivate(self):
        self.MainContent.setCurrentIndex(1)

    def ManagingActivate(self):
        self.MainContent.setCurrentIndex(2)

    def SettingsActivate(self):
        self.MainContent.setCurrentIndex(3)

        
if __name__ == "__main__":
    App = QApplication(sys.argv)
    
    # Dark theme
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(18, 18, 18))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255, 153))
    App.setPalette(palette)
    
    Root = MainWindow()
    Root.show()
    App.exec()