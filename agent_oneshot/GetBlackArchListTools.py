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

#Abrir archivos, recorremos y guardamos
with open("blackarch-tools.txt","a+") as out:
    with open("blackarch-tools.csv","a+") as csv:
        csv.write("Tool,Version,Category,URL\n")

        for tool in tools.items():  
            cols = tool('td')  
            if len(cols) >= 3: 
                name = cols.eq(0).text().strip()  
                version = cols.eq(1).text().strip() 
                description = cols.eq(2).text().strip()
                url = cols.eq(4).find('a').attr('href')
                category = cols.eq(3).text().strip()

                # Imprimimos los resultados
                print(f"Tool: {name}")
                print(f"Version: {version}")
                print(f"Category: {category}")
                print(f"Descripción: {description}")
                print(f"Url: {url}")
                print('-' * 50)

                #Guardamos en archivo texto grep
                out.write(f"Tool: {name}\n")
                out.write(f"Version: {version}\n")
                out.write(f"Category: {category}\n")
                out.write(f"Descripción: {description}\n")
                out.write(f"Url: {url}\n")
                out.write('-' * 50)
                out.write("\n")

                #Guardamos en archivo csv
                csv.write(f'"{name}","{version}","{category}","{url}"\n')

# Cerramos los archivos
csv.close()
out.close()




