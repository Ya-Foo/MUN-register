from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget

import cv2
import sys

class MainWindow(QWidget):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        
        self.VBL = QVBoxLayout()
        
        # widget to store camera feed
        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel)
        
        self.Thread1 = Thread()
        self.Thread1.start()
        self.Thread1.ImageUpdate.connect(self.ImageUpdateSlot)
        
        self.setLayout(self.VBL)
        
    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))
        
    def CancelFeed(self):
        self.Thread1.stop()
        
class Thread(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self) -> None:
        self.ThreadActive = True
        detector = cv2.QRCodeDetector()
        capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        while self.ThreadActive:
            ret, frame = capture.read()
            if ret:
                # QR code detection and decoding
                success, decode, pts, _ = detector.detectAndDecodeMulti(frame)
                if success:
                    for data, p in zip(decode, pts):
                        if data:
                            frame = cv2.polylines(frame, [p.astype(int)], True, (0, 255, 0), 8)
                            
                # Convert img into PyQT format and emit to main
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                Convert2QtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                pic = Convert2QtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(pic)
        capture.release()
    
    def stop(self):
        self.ThreadActive = False
        self.quit()
        
if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())