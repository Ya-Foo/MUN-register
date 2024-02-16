from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from settings import *
import api

class Register(QThread):
    def __init__(self, scanned: list) -> None:
        super(Register, self).__init__()
        self.scanned = scanned
        
    def run(self) -> None:
        for identifier in self.scanned:
            _, room, row = all_members[identifier]
            cell = f"'{room}'!{attendance_register_col}{row}"
            lookup_cell = f"'{room}'!{attendance_lookup_col}{row}"
            lookup_identifier = api.get_values(creds, sheets_id, lookup_cell)
            if identifier == lookup_identifier[0][0]: # validation if scanned QR is actual member
                api.write_values(creds, sheets_id, cell, 'USER_ENTERED', present)
        self.quit()