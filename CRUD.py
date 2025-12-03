from google.cloud import bigtable
from google.cloud.bigtable import row_filters
from google.cloud.bigtable.row_set import RowSet
import random

project_id = "project-60099802-d8b5-4aa9-a90"
instance_id = "hbitossaludmental"
table_id = "habitos_salud"

client = bigtable.Client(project=project_id, admin=False)
instance = client.instance(instance_id)
table = instance.table(table_id)

def impresionFila(fila):
    print(f"Clave de fila: {fila.row_key.decode('utf-8')}")
    # Itera sobre las familias de columnas y las celdas
    for column_family_id, column_family in fila.cells.items():
        print(f"  Familia de columnas: {column_family_id}")
        for column_id, cells in column_family.items():
            for cell in cells:
                print(f"    {column_id.decode('utf-8')}: {cell.value.decode('utf-8')}")
   
#Escritura
def escritura():
    age = input("Ingresa tu edad: ")
    gender = input("Ingresa 'm' para masculino y 'f' para femenino: ")
    
    if gender == 'm':
        gender = 'Male'
    else:
        gender = 'Female'
    
    days_wout_sm = input("Ingresa el número de días a la semana que no usas redes sociales: ")
    screen_time = input("Ingresa tus horas promedio de tiempo en pantalla por día: ")
    sm_platform = input("Ingresa la plataforma de redes sociales que usas con mayor frecuencia: ")
    exercise_freq_week = input("Ingresa cuántos días haces ejercicio a la semana: ")
    sleep_quality = input("Ingresa tu calidad de sueño del 1 al 10: ")
    stress_level = input("Ingresa tu nivel de estres del 1 al 10: ")
    happines_index = input("Ingresa tu nivel de felicidad del 1 al 10: ")

    row_key = f"{screen_time}#{exercise_freq_week}#{sleep_quality}#{random.randint(502, 10000)}"
    row = table.direct_row(row_key)

    row.set_cell("demographic_data", "age", age)
    row.set_cell("demographic_data", "gender", gender)

    row.set_cell("tech_use", "days_wout_sm", days_wout_sm)
    row.set_cell("tech_use", "screen_time", screen_time)
    row.set_cell("tech_use", "sm_platform", sm_platform)

    row.set_cell("habits", "exercise_freq_week", exercise_freq_week)
    row.set_cell("habits", "sleep_quality", sleep_quality)
    row.set_cell("habits", "stress_level", stress_level)

    row.set_cell("happines", "happines_index", happines_index)

    row.commit()
    print(f"La fila {row_key} se escribio correctamente.")


#Lectura
def lecturaConClave():
    clave = input("Ingresa la clave de la fila  que quieres visualizar: ")
    fila = table.read_row(clave)

    if (fila):
        impresionFila(fila)

        print()
        print("Impresion del indice de felicidad de la fila: ")
        col_filter = row_filters.ColumnQualifierRegexFilter(b"happines_index")
        fila = table.read_row(clave, filter_=col_filter)
        impresionFila(fila)
    else:
        print("No se encontro la fila.")
    

#{screen_time}#{exercise_freq_week}#{sleep_quality}#{random.randint(502, 10000)}"
def lectura():

    print("Impresion de las filas con un screen time de 7: ")
    prefix = "7.0#"
    end_key = prefix[:-1] + chr(ord(prefix[-1]) + 1)
    row_set = RowSet()
    row_set.add_row_range_from_keys(prefix.encode("utf-8"), end_key.encode("utf-8"))

    filas = table.read_rows(row_set=row_set)
    for fila in filas:
        impresionFila(fila)


    c = input("enter para continuar y ver las filas con 2 o 3 horas de uso diario en pantallas: ")

    print("Filas con 2 o 3 horas de uso diario de pantallas: ")
    
    filas = table.read_rows(
        filter_=row_filters.RowKeyRegexFilter(r"^(2\.0|3\.0)#.*".encode("utf-8"))
    )
    for fila in filas:
        impresionFila(fila)


def actualizar():
    clave = input("Ingresa la clave de la fila que se va a actualizar: ")
    fila = table.row(clave)

    print("Antes del cambio")
    impresionFila(table.read_row(clave))

    age = input("Ingresa la nueva edad: ")
    sleep_quality = input("Ingresa la nueva calidad de sueño(del 1 al 10): ")
    fila.set_cell("demographic_data", "age", age)
    fila.set_cell("habits", "sleep_quality", sleep_quality)
    fila.commit()

    print("Despues del cambio")
    impresionFila(table.read_row(clave))



def borrar():
    clave = input("Ingresa la clave de la fila que quieres borrar: ")
    fila = table.row(clave)
    fila.delete()
    fila.commit()
    print("La fila se borro exitosamente.")









