import cv2
from pyzbar import pyzbar
import pyodbc
from playsound import playsound
from tkinter import *
import datetime

#IMPORTACION DE RELOJ


conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:qa-centrolaboral-db.6ff6bdb9798a.database.windows.net,1433;DATABASE=CONTROL_DE_ASISTENCIA;UID=dtictiusr;PWD=P'T.j$4hdFU5X}u%m.gU")

def popUpNombre(qrcode_info):

    try:

        num_empleado1 = qrcode_info.replace('{',
                                            '')
        num_empleado2 = num_empleado1.replace('}', '')

        cursor = conn.cursor()

        #EXTRAER INFORMACIÓN DE LA BASE DE DATOS CUANDO EL QR YA CHECO
        cursor.execute(f"""SELECT CONCAT(NOMBRE,' ',APELLIDO_PATERNO,' ',APELLIDO_MATERNO) as Funcionario,
                        PUESTO, ADSCRIPCION,
                        case
                        when ID_STATUS = 0 then 'Inactivo'
                        when ID_STATUS = 1 then 'Activo' end as Estatus,
                        ID_EMPLEADO
                        FROM EMPLEADOS
                        WHERE ID_EMPLEADO = {num_empleado2}""")

        datos_usuario = cursor.fetchall()

        for row in datos_usuario:
            nombre=row[0]
            puesto=row[1]
            adscripcion=row[2]
            estatus = row[3]
            id_empleado= row[4]
#NOMBRE DE LA VENTANA
        window = Tk()
        window.title("CONTROL DE ASISTENCIA  CFCRL")

        lbl = Label(window, text="Funcionario: "+nombre)
        lbl.grid(column=0, row=0)

        lbl2 = Label(window, text="Puesto: "+puesto)
        lbl2.grid(column=0, row=1)

        lbl3 = Label(window, text="Adscripción: " + adscripcion)
        lbl3.grid(column=0, row=2)

        lbl4 = Label(window, text="Status: " + estatus)
        lbl4.grid(column=0, row=3)

        window.mainloop()

        hoy = datetime.date.today().strftime("%Y%m%d")

        maniana = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y%m%d")

        try:
            cursor2 = conn.cursor()
            cursor2.execute(
                f"select ID_ASISTENCIA from ASISTENCIA where ID_EMPLEADO = {id_empleado} and ENTRADA between '"+hoy+"' and '"+maniana+"'")
            id_asistencia = cursor2.fetchone()


            cursor3 = conn.cursor()
            cursor3.execute(
                "update ASISTENCIA set SALIDA  = getdate() where ID_ASISTENCIA = " + str(id_asistencia[0]))
            conn.commit()
            if(id_empleado==633):
                # AUDIO PARA SALIDA TORBE
                sonido = "C:\\CONTROL_DE_ASISTENCIA\\LectorQR\\torbe.mp3"
                playsound(sonido)
            elif (id_empleado ==1):
                # AUDIO PARA SALIDA LIC-MARRUFO
                sonido = "C:\\CONTROL_DE_ASISTENCIA\\LectorQR\\SALIDA_ADM.mp3"
                playsound(sonido)



            else:

                # AUDIO PARA SALIDA
                sonido = "C:\CONTROL_DE_ASISTENCIA\LectorQR\AUDIO_SALIDA.mp3"
                playsound(sonido)



        except:
            cursor4 = conn.cursor()
            cursor4.execute(
                "insert into ASISTENCIA(ID_EMPLEADO, ENTRADA) values(" + num_empleado2 + ", GETDATE()) SELECT * FROM EMPLEADOS WHERE ID_EMPLEADO = " + num_empleado2 + ";")
            conn.commit()

            if (id_empleado == 633):
                # AUDIO PARA ENTRADA TORBE
                sonido = "C:\\CONTROL_DE_ASISTENCIA\\LectorQR\\Torbe_entrada.mp3"
                playsound(sonido)
            elif (id_empleado == 1):
                # AUDIO PARA ENTRADA LIC-MARRUFO
                sonido = "C:\\CONTROL_DE_ASISTENCIA\\LectorQR\\BIENVENIDO_LIC_ADM.mp3"
                playsound(sonido)

            else:

                #AUDIO PARA QR CORRECTO
                sonido = "C:\CONTROL_DE_ASISTENCIA\LectorQR\BIENVENIDO.mp3"
                playsound(sonido)

#AUDIO PARA QR INCORRECTO
    except:
        sonido = "C:\CONTROL_DE_ASISTENCIA\LectorQR\ACCESO_NO_VALIDO.mp3"
        playsound(sonido)

def read_qrcode(frame):
    qrcodes = pyzbar.decode(frame)
    for qrcode in qrcodes:
        x,y,w,h = qrcode.rect

        qrcode_info = qrcode.data.decode("latin1")
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame,qrcode_info, (x+6,y-6), font, 2.0, (255,255,255),1)

        with open("qr_code.txt", "w", encoding="utf-8") as file:
            file.write("Trajo esta info: " + qrcode_info)

        popUpNombre(qrcode_info)

    return frame

def encender_camara():

    camara = cv2.VideoCapture(0)
    ret, frame = camara.read()

    while ret:
        ret, frame = camara.read()
        frame = read_qrcode(frame)
        cv2.imshow('Lector de QR', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    camara.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    encender_camara()

