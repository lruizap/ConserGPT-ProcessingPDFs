import fitz  # PyMuPDF
import io

def limpiar_y_convertir_a_txt(input_path, output_txt_path):
    doc = fitz.open(input_path)
    texto_completo = ""

    for pagina_num in range(doc.page_count):
        pagina = doc[pagina_num]
        texto_pagina = pagina.get_text()

        # Buscar la posición de las palabras clave
        inicio_eliminar = texto_pagina.find("FIRMADO POR")
        fin_eliminar = texto_pagina.find("Es copia auténtica de documento electrónico") + len("Es copia auténtica de documento electrónico")

        # Eliminar la sección específica
        texto_pagina = texto_pagina[:inicio_eliminar] + texto_pagina[fin_eliminar:]

        texto_completo += texto_pagina

    # Guardar el texto en un archivo de texto
    with io.open(output_txt_path, "w", encoding="utf-8") as archivo_txt:
        archivo_txt.write(texto_completo)

    doc.close()

# Uso del método
input_pdf = "./pdf_folder/Instruccion26septiembre2023PremiosExtraordinariosMusica.pdf"
output_txt = "./salida/Instruccion26septiembre2023PremiosExtraordinariosMusica.txt"

limpiar_y_convertir_a_txt(input_pdf, output_txt)