# Import PyQT
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget

import sys

# Import from Python files
from qrRead import QRThread

class MainWindow(QWidget):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        
        self.VBL = QVBoxLayout()
        self.setWindowTitle("MUN Registration")
        
        # widget to store camera feed
        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel)
        
        # widget to retrieve & display scanned info
        self.InfoLabel = QLabel()
        self.VBL.addWidget(self.InfoLabel)
        
        # Updating the widgets
        self.Thread1 = QRThread()
        self.Thread1.start()
        self.Thread1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.Thread1.InfoUpdate.connect(self.TextUpdateSlot)
        
        self.setLayout(self.VBL)
        self.showMaximized()
        
    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))
        
    def TextUpdateSlot(self, Text:str):
        self.InfoLabel.setText(Text)
        
    def CancelFeed(self):
        self.Thread1.stop()

        
if __name__ == "__main__":
    # Main app
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())