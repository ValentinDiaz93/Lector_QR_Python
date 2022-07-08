#RELOJ VDC
#LIBRERIAS IMPORTADAS
from tkinter import Label, Tk
from time import strftime



def reloj_fecha():


    ventana = Tk()
    ventana.title('Reloj Control de Asistencia CFCRL')  #TITULO DE LA VENTANA
    ventana.config(bg='black') #white
    ventana.geometry('350x200+10+10') #TAMAÑO DE LA VENTANA
    ventana.minsize(width=250, height=200)  #DIMENSIONES MINIMAS



    ventana.columnconfigure(0, weight=15)
    ventana.rowconfigure(0, weight=15)

    ventana.columnconfigure(0, weight=1)
    ventana.rowconfigure(1, weight=1)

    ventana.columnconfigure(0, weight=1)
    ventana.rowconfigure(2, weight=1)



#-------------------------------------------------------
    #Aqui se agrego el espacio del para el texto de CFCRL
    ventana.columnconfigure(0, weight=1)
    ventana.rowconfigure(3, weight=1)
 # -------------------------------------------------------

    #FUNCION PARA OBTENER TIEMPO
    def obtener_tiempo():
        hora = strftime('%H:%M:%S')
        dia = strftime('%A')
        fecha = strftime('%d - %m - %y')

    #AL VARIAR LA PANTALLA LOS PIXELES VARIAN
        x = texto_hora.winfo_height()
        t = int((x - 5) * 0.32)

        if dia == 'Monday':
            dia = 'Lunes'

        elif dia == 'Tuesday':
            dia = 'Martes'

        elif dia == 'Wednesday':
            dia = 'Miercoles'

        elif dia == 'Thursday':
            dia = 'Jueves'

        elif dia == 'Friday':
            dia = 'Viernes'

        elif dia == 'Saturday':
            dia = 'Sábado'

        elif dia == 'Sunday':
            dia = 'Domingo'

        texto_hora.config(text=hora, font=('Consolas', t)) #Radioland
        texto_dia.config(text=dia)
        texto_fecha.config(text=fecha)



        texto_hora.after(1000, obtener_tiempo)

    #HORA

    texto_hora = Label(ventana, fg='#E6E0D4', bg='#235B4E')  #color de numeros (fg) y de fondo  (bg)
    texto_hora.grid(row=0, sticky="nsew", ipadx=5, ipady=20)

    #DIA LUNES  A VIERNES CON LETRA
      #fg es el color del dia  bg es el color de fondo de viernes
    texto_dia = Label(ventana, fg='#E6E0D4', bg='BLACK', font=('Consolas', 20))  #Lucida Calligraphy'
    texto_dia.grid(row=1, sticky="nsew")


    #FECHA  DIA MES AÑO
    texto_fecha = Label(ventana, fg='green2', bg='#235B4E', font=('Consolas', 20, 'bold')) #Comic Sans MS
    texto_fecha.grid(row=2, sticky="nsew")



#-----------------------------------------------------------------------

    texto_cfcrl = Label(ventana, text="CONTROL DE ASISTENCIA CFCRL", fg='#235B4E', bg='#E6E0D4',
                        font=('Consolas', 16, 'bold'))  # Comic Sans MS


    texto_cfcrl.grid(row=3, sticky="nsew")   #row indica la posicion donde esta
    #texto_cfcrl.pack(fill=Tk.X)


    #-----------------------------------------------------------------------
    obtener_tiempo()
    ventana.mainloop()



if __name__=="__main__":
    reloj_fecha()
