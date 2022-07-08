import tkinter as tk                         #libreria tkinter
ventana=tk.Tk()                              #definir ventana
ventana.title("Ventana de prueba 1")         #titulo de la ventana
ventana.geometry("380x380")                  #Tamaño de la ventena     ancho por alto
ventana.configure(background="lawn green")   #Color de fondo de la ventana

etiqueta1=tk.Label(ventana,text="TEXTODESEADO",bg="magenta",fg="black") #llamas a la etiqueta(label), texto que desea simprimir, color de fondo, color de texto
etiqueta1.pack(fill=tk.X)   #El fill llena todo el eje de X


##de aqui en adelaante solo se repite

etiqueta2=tk.Label(ventana,text="TEXTODESEADO",bg="magenta",fg="black") #llamas a la etiqueta(label), texto que desea simprimir, color de fondo, color de texto
etiqueta2.pack(padx=20,pady=20)    #da espacio En eje X e Y


etiqueta3=tk.Label(ventana,text="TEXTODESEADO",bg="magenta",fg="black") #llamas a la etiqueta(label), texto que desea simprimir, color de fondo, color de texto
etiqueta3.pack(side=tk.LEFT)    #Alineamos la etiqueta


etiqueta4=tk.Label(ventana,text="TEXTODESEADO",bg="magenta",fg="black") #llamas a la etiqueta(label), texto que desea simprimir, color de fondo, color de texto
etiqueta4.pack(padx=20,pady=20,ipadx=5,ipady=5)    #da espacio En eje X e Y  y el ipad  da espaciosdentro de la etiqueta


ventana.mainloop()                           #Hace que se cree un ciclo infinito, que mientras no se cierre la ventana todo se sigue ejecutando


#if __name__=="__main__":