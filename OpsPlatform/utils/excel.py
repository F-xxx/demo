# -*- coding:utf-8 -*-  

def SheetWrite(sheet, row, serverasset, style):
    sheet.write(row,0, serverasset.hostnam, style)
    sheet.write(row,1, serverasset.ip_addr, style)
    sheet.write(row,2, serverasset.cpu, style)
    sheet.write(row,3, serverasset.memory, style)
    sheet.write(row,4, serverasset.disk, style)
    sheet.write(row,4, serverasset.system_type, style)
    sheet.write(row,5, serverasset.idc, style)

