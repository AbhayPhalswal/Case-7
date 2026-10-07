import openpyxl
def load(path):
    ws = openpyxl.load_workbook(path, data_only=True)["Data"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[0]
    return [dict(zip(hdr, r)) for r in rows[1:]]
