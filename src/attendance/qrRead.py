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
from PyQt5.QtCore import *

import cv2, pyautogui

from settings.settings import *
import api

# Constants
width, height = pyautogui.size()

class QRRead(QThread):
    # Initialise thread's signals
    ImageUpdate = pyqtSignal(QImage)
    InfoUpdate = pyqtSignal(str)
    NameUpdate = pyqtSignal(str)
    
    def run(self) -> None:
        self.ThreadActive = True
        detector = cv2.QRCodeDetector()
        capture = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        while self.ThreadActive:
            ret, frame = capture.read()
            if ret:
                # Flip camera if using webcam
                if cam_id == 0:
                    frame = cv2.flip(frame, 1)
                # QR code detection and decoding
                success, decode, pts, _ = detector.detectAndDecodeMulti(frame)
                if success:
                    for data, p in zip(decode, pts):
                        if data:
                            frame = cv2.polylines(frame, [p.astype(int)], True, (0, 255, 0), 8)
                            self.InfoUpdate.emit(data)
                            try:
                                self.NameUpdate.emit(all_members[data][0])
                                self.registerThread = Register(data)
                                self.registerThread.start()
                            except:
                                self.NameUpdate.emit("Member not found")
                            
                # Convert img into PyQT format and emit to main
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                Convert2QtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                pic = Convert2QtFormat.scaled(width//5*4, height//3*2)
                self.ImageUpdate.emit(pic.copy())
        capture.release()
    
    def stop(self) -> None:
        self.ThreadActive = False
        self.quit()


class Register(QThread):    
    def __init__(self, identifier: str) -> None:
        super(Register, self).__init__()
        self.identifier = identifier
        
    def run(self) -> None:
        _, room, row = all_members[self.identifier]
        cell = f"'{room}'!{attendance_register_col}{row}"
        lookup_cell = f"'{room}'!{attendance_lookup_col}{row}"
        lookup_identifier = api.get_values(creds, sheets_id, lookup_cell)
        # validation if scanned QR is actual member
        if self.identifier == lookup_identifier[0][0].rstrip():
            api.write_values(creds, sheets_id, cell, 'USER_ENTERED', present)
        self.quit()