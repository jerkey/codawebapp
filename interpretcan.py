import cantools
import re

can0_db = cantools.database.load_file('CODA-B-CAN.dbc')
can1_db = cantools.database.load_file('CODA-C-CAN-cells.dbc')
can1_db.add_dbc_file('CODA-D-CAN.dbc')

class can_db:
    def __init__(self, dbc_file):
        self.db = cantools.database.load_file(dbc_file)

    def add_dbc(self, dbc_file):
        self.db.add_dbc_file(dbc_file)


def interpretCandumpTALine(line, db):
    notimeline = re.sub(r'^\s*\([^)]*\)', '', line).strip()
    m = re.match(r'^\s*(\S+)\s+([0-9A-F]+)\s*\[\d+\]\s*([0-9A-F ]*)$', notimeline)
    try:
        frame_id = int(m.group(2), 16)
        data     = bytes.fromhex(m.group(3).replace(' ', ''))
        msg = db.get_message_by_frame_id(frame_id)
        decoded = msg.decode(data, decode_choices=True)
    except:
        decoded = line
    return decoded

if __name__ == "__main__":
    line = " (2026-09-13 21:02:36.849770)  can0  381   [8]  0C CE 0C DF 0C 70 3D 37"
    print(interpretCandumpTALine(line, can0_db))
# {'AvgCellVoltage': 3278, 'MaxCellVoltage': 3295, 'MinCellVoltage': 3184, 'VmaxId': 61, 'VminId': 55}
