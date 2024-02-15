import json

import api

with open("src/config.json", 'r') as f:
    creds = api.auth()
    data = json.loads(f.read())
    cam_id = data["camera_id"]
    sheets_id = data["sheets_id"]
    
    all_members_info = data["info"]
    all_members_page = all_members_info["page"]
    all_members_start = all_members_info["start_row"]
    all_members_cell = f"'{all_members_page}'!A{str(all_members_start)}:B1000"
    all_members = {}
    for identifier, name in api.get_values(creds, sheets_id, all_members_cell):
        all_members[identifier] = name
        
    attendance_info = data["attendance"]
    attendance_rooms = attendance_info["rooms"]
    attendance_lookup_col = attendance_info["identifier_column"]
    attendance_register_col = attendance_info["register_column"]
    attendance_start = attendance_info["start_row"]
    attendance_cells = []
    for room in attendance_rooms:
        cells = f"'{room}'!{attendance_lookup_col}{str(attendance_start)}:{attendance_register_col}1000"
        attendance_cells.append(cells)