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

import json
import re

import api

with open("src/settings/config.json", 'r') as f:
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
        all_members[identifier.rstrip()] = [name.rstrip(), f"Room {room}"]
        
    session_info = data["session"]
    attendance_rooms = session_info["rooms"]
    attendance_lookup_col = session_info["identifier_column"]
    attendance_register_col = session_info["register_column"]
    attendance_start = session_info["start_row"]
    for room in attendance_rooms:
        cell = f"'{room}'!{attendance_lookup_col}{attendance_start}:{attendance_lookup_col}1000"
        room_members = [i[0] for i in api.get_values(creds, sheets_id, cell)]
        for index, member in enumerate(room_members):
            all_members[member.rstrip()].append(index+attendance_start)
            
    country_col = session_info["country_column"]
    amendment_col = session_info["amendment_column"]
    speech_col = session_info["speech_column"]
    poi_col = session_info["poi_column"]

    present = data["present_marker"]