import io
import re
import requests
from PyPDF2 import PdfReader

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Windows; Windows x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'}

url = 'https://www.adideandalucia.es/normas/ordenes/Orden15abril2011SubvencionesAsociaciones.pdf'
response = requests.get(url=url, headers=headers, timeout=120)
on_fly_mem_obj = io.BytesIO(response.content)
pdf_file = PdfReader(on_fly_mem_obj)

# Crear un archivo Markdown
markdown_content = ""

# Variable para rastrear si nos encontramos en la sección de anexos
en_anexos = False

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

    text = re.sub(r'Artículo', '# Artículo', text)

    # Verificar si estamos en la sección de anexos
    if re.search(r'ANEXO', text):
        en_anexos = True

    # Excluir la sección de anexos del contenido final
    if not en_anexos:
        markdown_content += text

# Guardar el contenido Markdown en un archivo
with open("output.md", "w", encoding="utf-8") as markdown_file:
    markdown_file.write(markdown_content)

print("Conversion completa. Archivo Markdown generado: output.md")
