<div align="center">
	Universidad Autónoma de Yucatán<br>
	Facultad de Matemáticas UADY
	<h4>Proyecto Integrador</h4>
	<h3>MODELADO DE DATOS</h3>
  	<img src="logouady.png" alt="Logo UADY" width="200"><br>
</div>

<br></br>
**Integrantes de Equipo:**

* Andrea Baeza Estrella
* Julián Alejandro Rodríguez Jaime
* Adrián Vázquez Martínez

<div align="right">
	Fecha de Entrega: 03/12/2025
</div>

# Dataset 
 El [dataset](https://www.kaggle.com/datasets/prince7489/mental-health-and-social-media-balance-dataset) busca capturar la relación que existe entre los hábitos de las personas, incluido el uso de redes sociales y plataformas digitales, con su salud mental. 
 ## Diccionario de datos: 
| Familia | Nombre | Descripción |  Tipo de dato
| ----------- | ----------- | ----------- |  -----------
| User_ID | User_ID | Identificador único de usuario registrado. |  VARCHAR(4)
| demographic_data | Age | Edad del usuario. | INT
| demographic_data | Gender | Género del usuario. | VARCHAR(8)
| technology_use | Daily_Screen_Time | Cantidad de tiempo que el usuario pasa en redes sociales y/o algún dispositivo electrónico. | FLOAT
| habits | Sleep_Quality | Calidad de sueño del usuario. Valor entre 1-10. | INT
| habits | Stress_Level | Nivel de estrés del usuario. Valor entre 1-10. | INT
| technology_use | Days_Without_Social_Media | Días que el usuario ha pasado sin usar redes sociales | INT
| habits | Exercise Frequency | Días de la semana que el usuario hace ejercicio | INT
| technology_use | Social_Media_Platform | La plataforma que el usuario usa con mayor frecuencia | VARCHAR(30)
| Happines_Index | Happines_Index | Índice de felicidad. Valor entre 1-10. | INT
# Modelado del dataset
La elección del dataset se realizó tanto por nuestro interés en el tema, como porque las características se adaptan muy bien a BigTable, ya que:
- Los datos ya están organizados en el modelo clave-valor.
- Solo es una tabla, por lo que no hay necesidad de hacer relaciones entre tablas.
- Resulta intuitivo organizar las columnas existentes en familias de columnas.
- La mayoría de los datos son numéricos.

No buscamos un dataset muy grande a pesar de que BigTable está optimizado para trabajar con grandes cantidades de datos debido a que el manejo de mayores cantidades de datos podría llegar a ser muy costoso, por lo que, para propósitos del proyecto, preferimos optar por un dataset pequeño que siga mantiendo las demás características que lo hacen ideal para el servicio.

Tomando esto en cuenta, nuestro modelado del dataset para adaptarlo a BigTable fue el siguiente:

![Esquema de la base](esquema_habitossalud.jpeg)

> **hacer tabla de nuestro modelo :**  me basare en la del diccionario, por eso no la hice.
## Elección de la clave de fila
Esta es una parte importante del diseño de una base de datos en BigTable ya que los querys basados en clave de fila son los mas eficientes en bigTable debido a que la base ordena los datos en base a sus claves de filas.

Es por esto que es recomendable diseñar un clave de fila que comience con los datos con los cuales estaremos haciendo querys mas comunmente ya que asi simplemente podremos buscar que filas corresponde a cierto prefijo de clave de fila (o a cierta expresion regular) y asi encontrar los datos deseados, esto se ve mas a detalle en la seccion de sentencias.

Tomando esto en cuenta nosotros diseñamos el siguiente clave de fila: #screen_time#exercise_freq_week#sleep_quality#UID 
Poniendo al inicio los datos mediante los cuales realizaremos querys y al final incluyendo el id del csv original para asegurar que cada clave de fila sea unica.

# Proceso de importacion
El proceso de importación consistió en varios pasos, las herramientas utilizadas están en negrita:
1. Se creó la base de datos, esto implicó crear una cuenta nueva en Google Cloud, reclamar los 300 dólares de crédito que se ofertan como prueba gratis, y crear la tabla, configurándola para que el costo fuera el más bajo posible para que no exceder nuestro presupuesto al terminar el proyecto.
2.  Dentro de la consola de **Google Cloud** se configuro el **Cloud Shell** para tener acceso a nuestra base de datos.
3.  Se crearon las columnas del Schema a través de sentencias como las que se incluyen en la 
[seccion de sentencias](#Sentencias) de este README.
4. Se creó un [script](https://github.com/andybaeza/proyecto-E04/blob/main/dataloader.py) de Python que realiza la importación del csv descargado de Kaggle a nuestra base, tomando en cuenta las familias de columnas y la clave de fila que definimos al inicio.

# Sentencias
Todo el codigo de las sentencias fue basado en la [documentación](https://docs.cloud.google.com/bigtable/docs) que google ofrece para trabajar con bigTable desde python.

El archivo [CRUD.py](https://github.com/andybaeza/proyecto-E04/blob/main/CRUD.py) de este repositorio tiene todo el codigo del funcionamiento CRUD del proyecto, a continuacion se encuentran algunos fragmentos: 

### Create
El siguiente codigo de python es una funcion que al llamarla le pide al usuario los datos de una fila y posteriormente la ingresa en la base de datos.

```python
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
```

### Read
Encuentra las filas que tienen 2 o 3 de DailyScreenTime utilizando la clave de fila:

```python
  filas = table.read_rows(
        filter_=row_filters.RowKeyRegexFilter(r"^(2\.0|3\.0)#.*".encode("utf-8"))
    )
    for fila in filas:
        impresionFila(fila)
```

### Update

Actualiza los campos de age y sleep_quality de una fila, pidiendole al usuario los nuevos datos.

```python
	age = input("Ingresa la nueva edad: ")
    sleep_quality = input("Ingresa la nueva calidad de sueño(del 1 al 10): ")
    fila.delete_cell("demographic_data", "age")
    fila.set_cell("demographic_data", "age", age)
    fila.delete_cell("habits", "sleep_quality",)
    fila.set_cell("habits", "sleep_quality", sleep_quality)
    fila.commit()

```

### Delete 

Le pide una clave de fila al usuario y posteriormente borra esa fila.
```python
clave = input("Ingresa la clave de la fila que quieres borrar: ")
fila = table.row(clave)
fila.delete()
fila.commit()
```

# Referencias
* Mental Health & Social Media Balance Dataset. (2025). Kaggle. [https://www.kaggle.com/datasets/prince7489/mental-health-and-social-media-balance-dataset](https://www.kaggle.com/datasets/prince7489/mental-health-and-social-media-balance-dataset?utm_source=chatgpt.com)
* Google Cloud. (2025, mayo 10). _Hands on – Loading and Querying Data with Google Cloud Bigtable_ [Video]. YouTube. [https://youtu.be/9xGsRruTv5s](https://youtu.be/9xGsRruTv5s?utm_source=chatgpt.com)
* 
