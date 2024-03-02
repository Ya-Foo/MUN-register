# Import PyQT
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from segno import make_qr

# Import from Python files
from settings import all_members

class QRCreate(QThread):
    def run(self) -> None:
        for identifier, data in all_members.items():
            img = make_qr(identifier)
            img.save(f'qrcodes/{data[0]}.png',scale=10,border=1)
        self.quit()