# Import PyQT
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import json
import re

import api

with open("src/config.json", 'r') as f:
    creds = api.auth()
    data = json.loads(f.read())
    
    cam_id = data["camera_id"]
    sheets_url = data["sheets_url"]
    sheets_id = re.findall(".*/(.*)/", sheets_url)[0]

    all_members_info = data["info"]
    all_members_page = all_members_info["page"]
    all_members_start = all_members_info["start_row"]
    all_members_cell = f"'{all_members_page}'!A{str(all_members_start)}:C1000"
    all_members = {}
    for identifier, name, room in api.get_values(creds, sheets_id, all_members_cell):
        all_members[identifier] = [name.rstrip(), f"Room {room}"]
        
    attendance_info = data["attendance"]
    attendance_rooms = attendance_info["rooms"]
    attendance_lookup_col = attendance_info["identifier_column"]
    attendance_register_col = attendance_info["register_column"]
    attendance_start = attendance_info["start_row"]
    for room in attendance_rooms:
        cell = f"'{room}'!{attendance_lookup_col}{attendance_start}:{attendance_lookup_col}1000"
        room_members = [i[0] for i in api.get_values(creds, sheets_id, cell)]
        for index, member in enumerate(room_members):
            all_members[member].append(index+attendance_start)

    present = data["present_marker"]