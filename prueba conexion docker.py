import psycopg2

#CONEXION A BASE DE DATYOS POSTGRES
conn = psycopg2.connect(host='localhost',database='prueba',user='postgres',password='1802Diaz')





cursor = conn.cursor()
cursor.execute(f"""SELECT CONCAT(nombre,' ',apellido_paterno,' ',apellido_materno) as Funcionario,
                puesto, adscripcion,
                id_empleado
                FROM empleados
                WHERE id_empleado = 1""")
#fetchall  Muestra la informacion line apor linea  y fetchone  en una sola lina la informacion
datos_usuario = cursor.fetchall()

for row in datos_usuario:
    nombre = row[0]
    puesto = row[1]
    adscripcion = row[2]
    id_empleado = row[3]


print(nombre)
print(puesto)
print(adscripcion)
print(id_empleado)

