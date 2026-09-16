import cantools
import re

db = cantools.database.load_file('CODA-B-CAN.dbc')

line = " (2026-09-13 21:02:36.849770)  can0  381   [8]  0C CE 0C DF 0C 70 3D 37"
notimeline = re.sub(r'^\s*\([^)]*\)', '', line).strip()
m = re.match(r'^\s*(\S+)\s+([0-9A-F]+)\s*\[\d+\]\s*([0-9A-F ]*)$', notimeline)
frame_id = int(m.group(2), 16)
data     = bytes.fromhex(m.group(3).replace(' ', ''))
msg = db.get_message_by_frame_id(frame_id)
decoded = msg.decode(data, decode_choices=True)
print(decoded)
# {'AvgCellVoltage': 3278, 'MaxCellVoltage': 3295, 'MinCellVoltage': 3184, 'VmaxId': 61, 'VminId': 55}
