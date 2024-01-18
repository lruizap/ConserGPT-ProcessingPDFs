import io
import re
import json
import requests
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
from tabulate import tabulate

list_order_fem = ['PRIMERA', 'SEGUNDA', 'TERCERA', 'CUARTA', 'QUINTA', 'SEXTA', 'SÉPTIMA', 'OCTAVA', 'NOVENA', 'DÉCIMA',
                  'UNDÉCIMA', 'DUODÉCIMA', 'DECIMOTERCERA', 'DECIMOCUARTA', 'DECIMOQUINTA', 'DECIMOSEXTA', 'DECIMOSÉPTIMA',
                  'DECIMOCTAVA', 'DECIMONOVENA', 'VIGÉSIMA', 'VIGÉSIMA PRIMERA', 'VIGÉSIMA SEGUNDA', 'VIGÉSIMA TERCERA',
                  'VIGÉSIMA CUARTA', 'VIGÉSIMA QUINTA']

list_order_masc = ['Primero', 'Segundo', 'Tercero', 'Cuarto', 'Quinto', 'Sexto', 'Séptimo', 'Octavo', 'Noveno', 'Décimo',
                   'Undécimo', 'Duodécimo', 'Decimotercero', 'Decimocuarto', 'Decimoquinto', 'Decimosexto', 'Decimoséptimo',
                   'Decimoctavo', 'Decimonoveno', 'Vigésimo', 'Vigésimo primero', 'Vigésimo segundo', 'Vigésimo tercero',
                   'Vigésimo cuarto', 'Vigésimo quinto']

list_rumanos = ['I ', 'I I ', 'I I I ', 'I V ', 'V ', 'V I ', 'V I I ', 'V I I I ', 'I X ', 'X ',
                'X I ', 'X I I ', 'X I I I ', 'X I V ', 'X V ', 'X V I ', 'X V I I ', 'X V I I I ', 'X I X ', 'X X ',
                'X X I ', 'X X I I ', 'X X I I I ', 'X X I V ', 'X X V ']

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Windows; Windows x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'}

json_path = "./JSON/ConserGPT_DATA.json"

with open(json_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)


for module_key, module_value in data["modules"].items():
    for info in module_value["Info"]:
        for pdf_info in info["ListPDF"]:
            link_pdf = pdf_info["LinkPDF"]

            try:
                response = requests.get(
                    url=link_pdf, headers=headers, timeout=120)
                on_fly_mem_obj = io.BytesIO(response.content)
                pdf_file = PdfReader(on_fly_mem_obj)

            except PdfReadError as e:
                print(f"Error al leer el PDF ({link_pdf}): {e}")
                with open(f"./output/logs.txt", "w", encoding="utf-8") as logs_file:
                    logs_file.write(
                        f"Error al leer el PDF ({link_pdf}): {e}")
                continue

            # Crear un archivo Markdown
            markdown_content = ""

            # Variable para rastrear si nos encontramos en la sección de anexos
            en_anexos = False

            # Función para agregar "#" delante de las palabras encontradas

            def agregar_hashtag(match):
                return '# ' + match.group(0)

            for pageNum in range(len(pdf_file.pages)):
                currentPage = pdf_file.pages[pageNum]
                text = currentPage.extract_text()

                # Eliminar encabezados y pies de página
                text = re.sub(
                    r'(\n|\s|^)([0-9]+|www\..+\.es)(\s|\n|$)', ' ', text, flags=re.MULTILINE)

                # Eliminar imágenes
                text = re.sub(r'\[image:.+?\]', '', text)

                # Eliminar guiones y saltos de línea subsiguientes
                text = re.sub(r'-\n', '', text)

                # Eliminar el contenido entre "FIRMADO POR" y "Es copia auténtica de documento electrónico"
                text = re.sub(r'FIRMADO POR.*?Es copia auténtica de documento electrónico',
                              '', text, flags=re.DOTALL)

                # Expresión regular para buscar el patrón "letra, paréntesis) y espacio"
                text = re.sub(r'([a-zA-Z])\)\s', '* ', text)

                # Elimina los cuadrados de eleccion vacios
                text = re.sub("˘", 'Falso: ', text)

                # Elimina el cuadrado de eleccion marcado (pero no la respuesta)
                text = re.sub("⾙", 'Verdadero: ', text)

                # Convertir los Artículos en títulos para las secciones
                text = re.sub(r'Artículo', '# Artículo', text)
                text = re.sub(r'INSTRUCCIONES', '# INSTRUCCIONES', text)

                # Patrón para buscar las palabras en la lista
                patron = re.compile(
                    r'\b(?:' + '|'.join(map(re.escape, list_order_fem)) + r')\b')

                # Reemplazar las palabras con "#" delante
                text = patron.sub(agregar_hashtag, text)

                # Patrón para buscar las palabras en la lista
                patron = re.compile(
                    r'\b(?:' + '|'.join(map(re.escape, list_order_masc)) + r')\b')

                # Reemplazar las palabras con "#" delante
                text = patron.sub(agregar_hashtag, text)

                # Patrón para buscar las palabras en la lista
                patron = re.compile(
                    r'\b(?:' + '|'.join(map(re.escape, list_rumanos)) + r')\b')

                # Reemplazar las palabras con "#" delante
                text = patron.sub(agregar_hashtag, text)

                if "Puntuaciones" in link_pdf:
                    lines = text.split('\n')

                    start_line = next((i + 1 for i, line in enumerate(lines)
                                       if "TURNON.ºD.N.I. APELLIDOS Y NOMBRE PUNTUACIÓNOBSERVACIONES" in line), None)

                    if start_line is not None:
                        headers = ["TURNO", "D.N.I.", "APELLIDOS Y NOMBRE",
                                   "PUNTUACIÓN", "OBSERVACIONES"]
                        filtered_lines = [line.strip().split(
                        ) for line in lines[start_line:] if line.startswith(("GENERAL", "DISCAPACIDAD"))]
                        text = tabulate(
                            filtered_lines, headers, tablefmt="pipe")

                # Verificar si estamos en la sección de anexos
                if re.search(r'ANEXO', text):
                    en_anexos = True

                # Excluir la sección de anexos del contenido final
                if not en_anexos:
                    markdown_content += text

            pdf_file.stream.close()

            # Guardar el contenido Markdown en un archivo
            if "https" in link_pdf:
                newName = link_pdf.replace(
                    'https://www.adideandalucia.es/normas/', '')
            else:
                newName = link_pdf.replace(
                    'http://www.juntadeandalucia.es/', '')

            newName = newName.replace('.pdf', '.md')
            newName = newName.replace('/', '_')

            with open(f"./output/documents/{newName}", "w", encoding="utf-8") as markdown_file:
                markdown_file.write(markdown_content)

            print("Conversion completa. Archivo Markdown generado:",
                  {link_pdf})
