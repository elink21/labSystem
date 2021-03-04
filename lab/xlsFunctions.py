from xlsxwriter.workbook import Workbook
import io
from . import dbFunctions as db


def getList(table: str) -> bytes:
    # Getting list from database
    data = db.getList(table)

    headers = {
        'students': ['id', 'Nombre', 'Numero de cuenta', 'Carrera'],
        'historiallendings': ['id', 'Fecha de devolucion','Fecha de prestamo', 'Numero de cuenta', 'Numero Patrimonial'],
        'items': ['id', 'Numero patrimonial', 'Nombre', 'Marca', 'Modelo', 'Stock'],
    }

    output = io.BytesIO()
    workbook = Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Writing headers
    header = headers[table]
    for i in range(len(header)):
        worksheet.write(0, i, header[i])

    for i in range(len(data)):
        for j in range(len(data[i])):
            worksheet.write(i+1, j, str(data[i][j]))
    workbook.close()
    output.seek(0)
    return [output,table]
