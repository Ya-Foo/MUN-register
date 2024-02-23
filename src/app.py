# https://www.youtube.com/watch?v=7DXxQV47jOU
# Import PyQT
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pyautogui, sys

# Import from Python files
from qrRead import QRRead
from qrCreate import QRCreate

# Constants
width, height = pyautogui.size()

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        
        self.setGeometry(0, 0, width, height)
        self.setWindowTitle("MUN App")
        
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
                                        font-size: 16pt;
                                        padding-top: 45px;
                                        padding-bottom: 45px;
                                        padding-left: 35px;
                                        color: #D3D3D3;
                                    }
                                    .QPushButton:hover{
                                        background-color: #1976D2;
                                    }
                                    """)
        self.SideMenu.setFixedWidth(width//5)
        self.MenuLayout = QVBoxLayout()
        self.MenuLayout.setSpacing(0)
        self.MenuLayout.setAlignment(Qt.AlignTop)
        self.MenuLayout.setContentsMargins(0, 0, 0, 0)
        
        # buttons in menu
        self.AttendanceBTN = QPushButton("Attendance")
        self.SessionBTN = QPushButton("Session Management")
        self.TaskBTN = QPushButton("Tasks Management")
        self.SettingsBTN = QPushButton("Settings")
        
        # add buttons to menu
        self.MenuLayout.addWidget(self.AttendanceBTN)
        self.MenuLayout.addWidget(self.SessionBTN)
        self.MenuLayout.addWidget(self.TaskBTN)
        self.MenuLayout.addWidget(self.SettingsBTN)
        self.SideMenu.setLayout(self.MenuLayout)
        
        # area for main contents
        self.MainContent = QFrame()
        self.MainContent.setStyleSheet(".QFrame{background-color: #121212}")
        self.MainContentLayout = QGridLayout()
        self.MainContentLayout.setSpacing(0)
        self.MainContentLayout.setContentsMargins(0, 0, 0, 0)
        self.MainContent.setLayout(self.MainContentLayout)
        
        # adding all to main application
        self.Grid.addWidget(self.SideMenu, 0, 0)
        self.Grid.addWidget(self.MainContent, 0, 1)
        
        
        
        self.setCentralWidget(self.CentralWidget)
        
        self.showMaximized()
        
if __name__ == "__main__":
    App = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
    Root = MainWindow()
    Root.show()
    App.exec()
    
# Notes:
# 4 main pages: Attendance, Settings, Task Completion, Session