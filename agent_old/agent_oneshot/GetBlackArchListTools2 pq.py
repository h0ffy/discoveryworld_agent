from pyquery import PyQuery as pq
import requests

# URL de la página que queremos scrapear
url = 'https://blackarch.org/tools.html'

# Hacemos la solicitud HTTP para obtener el contenido de la página
response = requests.get(url)

# Usamos PyQuery para parsear el HTML
doc = pq(response.text)

# Seleccionamos la tabla que contiene las herramientas
# Aquí, seleccionamos todas las filas de la tabla (tr), excluyendo la cabecera (primer fila)
tools = doc('table tr')

# Iteramos sobre las filas de la tabla, comenzando desde la segunda (para omitir el encabezado)
for tool in tools.items()[1:]:  # Omitimos la primera fila que es el encabezado
    cols = tool('td')  # Obtenemos todas las celdas de la fila
    if len(cols) >= 3:  # Nos aseguramos de que la fila tiene las tres columnas necesarias
        category = cols.eq(0).text().strip()  # Primera columna: Categoría
        name = cols.eq(1).text().strip()  # Segunda columna: Nombre de la herramienta
        description = cols.eq(2).text().strip()  # Tercera columna: Descripción
        
        # Imprimimos los rC