import cv2
from pyzbar import pyzbar
import pyodbc
from playsound import playsound
from tkinter import *

conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:qa-centrolaboral-db.6ff6bdb9798a.database.windows.net,1433;DATABASE=CONTROL_DE_ASISTENCIA;UID=dtictiusr;PWD=P'T.j$4hdFU5X}u%m.gU")

def fechone_lectura():
    cursor = conn.cursor()
    cursor.execute(f"""SELECT CONCAT(NOMBRE,' ',APELLIDO_PATERNO,' ',APELLIDO_MATERNO) as Funcionario,
                            PUESTO, ADSCRIPCION,
                            case
                            when ID_STATUS = 0 then 'Inactivo'
                            when ID_STATUS = 1 then 'Activo' end as Estatus,
                            ID_EMPLEADO
                            FROM EMPLEADOS
                            WHERE ID_EMPLEADO = 1""")

    datos_usuario = cursor.fetchall()

    for row in datos_usuario:
        nombre = row[0]
        puesto = row[1]
        adscripcion = row[2]
        estatus = row[3]
        id_empleado = row[4]


    try :
        print(id_empleado)

    except:
        print("No hay dato")

if __name__=="__main__":
    fechone_lectura()