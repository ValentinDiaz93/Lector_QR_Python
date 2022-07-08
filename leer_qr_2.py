import cv2
from pyzbar import pyzbar
import pyodbc      #conexion a base de datos sql
import psycopg2   #conexion a base de datos postgres
from playsound import playsound    #libreria para reproducir sonido de accceso
from tkinter import *
import datetime
#import ray
import Reloj
#import redis
from multiprocessing import Process
#import sys

# import reloj_final
# from time import strftime

#CONEXION A BASE DE DATOS SQL
#conn = pyodbc.connect(
    #"DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:qa-centrolaboral-db.6ff6bdb9798a.database.windows.net,1433;DATABASE=CONTROL_DE_ASISTENCIA;UID=dtictiusr;PWD=P'T.j$4hdFU5X}u%m.gU")
    #"DRIVER={SQL Server};SERVER=tcp:qa-centrolaboral-db.6ff6bdb9798a.database.windows.net,1433;DATABASE=CONTROL_DE_ASISTENCIA;UID=dtictiusr;PWD=P'T.j$4hdFU5X}u%m.gU")

#CONEXION A BASE DE DATOS POSTGRES
conn = psycopg2.connect(host='localhost',database='postgres',user='postgres',password='1802Diaz')

def popUpNombre(qrcode_info):
    global nombre, puesto, adscripcion, estatus, id_empleado
    try:

        num_empleado1 = qrcode_info.replace('{',
                                            '')
        num_empleado2 = num_empleado1.replace('}', '')
#se hace la primera conexion a la base de datos para traer informacion del usuario
        cursor = conn.cursor()
        cursor.execute(f"""SELECT CONCAT(nombre,' ',apellido_paterno,' ',apellido_materno) as Funcionario,
                        puesto, adscripcion,
                        id_empleado
                        FROM empleados
                        WHERE id_empleado = {num_empleado2}""")
#fetchall  Muestra la informacion linea por linea  y fetchone  en una sola lina la informacion
        datos_usuario = cursor.fetchall()

        for row in datos_usuario:
            nombre = row[0]
            puesto = row[1]
            adscripcion = row[2]
            id_empleado = row[3]
        # NOMBRE DE LA VENTANA
        window = Tk()

        #VENTANA EMERGENTE, DESPUES DE EL ACCESO
        window.title("CONTROL DE ASISTENCIA  CFCRL")
#
        lbl = Label(window, text="Funcionario: " + nombre)
        lbl.grid(column=0, row=0)

        lbl2 = Label(window, text="Puesto: " + puesto)
        lbl2.grid(column=0, row=1)

        lbl3 = Label(window, text="Adscripción: " + adscripcion)
        lbl3.grid(column=0, row=2)

      #  lbl4 = Label(window, text="Status: " + estatus)
       # lbl4.grid(column=0, row=3)

#TEMPORIZADOR DE CIERRE DE VENTANA
        window.after(3000,lambda :window.destroy())

        window.mainloop()

        hoy = datetime.date.today().strftime("%Y-%m-%d")

        maniana = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        try:
#AQUI COMIENZA A FALLAR
            cursor2 = conn.cursor()
            cursor2.execute(
                "select id_asistencia from asistencia where id_empleado = "+str(id_empleado)+" and entrada between '"+hoy+" 00:00:00.00' and '"+maniana+" 00:00:00.00'")
            id_asistencia = cursor2.fetchone()

#SE AGREGA UN AUDIO DE PRUEBA
           # playsound('C:/Audios/AUDIOPRUEBA.mp3')

            cursor3 = conn.cursor()
            cursor3.execute(
                f"update asistencia set salida  = now()::timestamp where id_asistencia = {str(id_asistencia[0])}")
            conn.commit()

            if (id_empleado == 633):
                # AUDIO PARA SALIDA TORBE       SE MODIFICARON LOS LINK DE LOS AUDIOS
                sonido = "C:/Audios/torbe.mp3"
                playsound('C:/Audios/torbe.mp3')
            elif (id_empleado == 1):
                # AUDIO PARA SALIDA LIC-MARRUFO  SE MODIFICARON LOS LINK DE LOS AUDIOS
                sonido = "C:/Audios/SALIDA_ADM.mp3"
                playsound('C:/Audios/SALIDA_ADM.mp3')



            else:

                # AUDIO PARA SALIDA   SE MODIFICARON LOS LINK DE LOS AUDIOS
                sonido = "C:/Audios/AUDIO_SALIDA.mp3"
                playsound('C:/Audios/AUDIO_SALIDA.mp3')



        except:

            cursor4 = conn.cursor()
            cursor4.execute(
                f"insert into asistencia(id_empleado, entrada) values({num_empleado2}, now()::timestamp)")
            conn.commit()

            if (id_empleado == 633):
                # AUDIO PARA ENTRADA TORBE    SE MODIFICARON LOS LINK DE LOS AUDIOS
                sonido = "C:/Audios/Torbe_entrada.mp3"
                playsound('C:/Audios/Torbe_entrada.mp3')
            elif (id_empleado == 1):
                # AUDIO PARA ENTRADA LIC-MARRUFO      SE MODIFICARON LOS LINK DE LOS AUDIOS
                sonido = "C:/Audios/BIENVENIDO_LIC_ADM.mp3"
                playsound('C:/Audios/BIENVENIDO_LIC_ADM.mp3')



            else:

                # AUDIO PARA QR CORRECTO           SE MODIFICARON LOS LINK DE LOS AUDIOS
                sonido = "C:/Audios/BIENVENIDO.mp3"
                playsound('C:/Audios/BIENVENIDO.mp3')

    # AUDIO PARA QR INCORRECTO    SE MODIFICARON LOS LINK DE LOS AUDIOS
    except:
        sonido = "C:/Audios/ACCESO_NO_VALIDO.mp3"
        playsound('C:/Audios/ACCESO_NO_VALIDO.mp3')


def read_qrcode(frame):
    qrcodes = pyzbar.decode(frame)
    for qrcode in qrcodes:
        x, y, w, h = qrcode.rect

        qrcode_info = qrcode.data.decode("latin1")
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, qrcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)

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


if __name__ == "__main__":
    # encender_camara()
    # ray.get([encender_camara(),Reloj.reloj_fecha()])

    p1 = Process(target=encender_camara)
    p1.start()
    p2 = Process(target=Reloj.reloj_fecha)
    p2.start()
    # This is where I had to add the join() function.
    p1.join()
    p2.join()
