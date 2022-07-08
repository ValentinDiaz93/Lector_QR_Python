import pandas as pd
import qrcode
from PIL import Image


def createQRCode():

    empleados = pd.read_csv("EMPLEADOS.csv")

    Logo_link = 'CFCRL_FV.png'

    logo = Image.open(Logo_link)

    basewidth = 200

    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)

    for index, values in empleados.iterrows():
        num_empleado = values["id_empleado"]
        apellido_paterno = values["apellido_paterno"]
        apellido_materno = values["apellido_materno"]
        nombre = values["nombre"]
        puesto = values["puesto"]
        adscripcion = values["adscripcion"]

        data = {num_empleado}

        image = qrcode.make(data)

        pos = ((image.size[0] - logo.size[0]) // 2,
               (image.size[1] - logo.size[1]) // 2)

        # image.paste(image, pos)
#NOMBRE CON EL CUAL SE GUARDARAN LOS QR
        image.save(f"QRs\\{num_empleado}_{apellido_paterno}_{apellido_materno}_{nombre}.png")

if __name__=='__main__':
    createQRCode()