from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from settings import *
import api

class Register(QThread):
    def __init__(self, scanned: list) -> None:
        super(Register, self).__init__()
        self.scanned = scanned
        self.registered = []
        
    def run(self) -> None:
        print("started")
        print(self.scanned)
        for room in attendance_rooms:
            start = attendance_start
            for identifier, data in all_members.items():
                if data[1] == room:
                    cell = f"'{room}'!{attendance_register_col}{start}"
                    lookup_cell = f"'{room}'!{attendance_lookup_col}{start}"
                    print(identifier, data, start, cell, lookup_cell)
                    lookup_identifier = api.get_values(creds, sheets_id, lookup_cell)
                    if identifier == lookup_identifier[0][0]:
                        if identifier in self.scanned:
                            print(identifier, start, cell, lookup_cell)
                            api.write_values(creds, sheets_id, cell, 'USER_ENTERED', present)
                        else:
                            api.write_values(creds, sheets_id, cell, 'USER_ENTERED', absent)
                    start += 1
        print("ended")
        self.quit()