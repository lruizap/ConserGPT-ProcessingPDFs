import fitz  # PyMuPDF


def extraer_texto_sin_pie_de_pagina(pdf_path, output_path):
    doc = fitz.open(pdf_path)

    for num_pagina in range(doc.page_count):
        pagina = doc[num_pagina]
        elementos_pagina = pagina.get_text("blocks")

        # Inicializar el texto de la página
        texto_pagina = ""

        for bloque in elementos_pagina:
            # Analiza las coordenadas y dimensiones del bloque
            x, y, width, height = bloque[:4]

            # Define un área que podría considerarse como pie de página
            # (Esto es un ejemplo, debes ajustarlo según tu caso específico)
            pie_de_pagina_area = (x, y, x + width, y + 20)

            # Comprueba si el bloque se superpone con el área del pie de página
            if (x >= pie_de_pagina_area[0] and x <= pie_de_pagina_area[2]) and \
               (y >= pie_de_pagina_area[1] and y <= pie_de_pagina_area[3]):
                # Si el bloque está en el área del pie de página, no lo añade al texto
                continue

            # Agrega el texto del bloque al texto de la página
            texto_pagina += bloque[4]

        # Guarda el texto de la página en un nuevo documento
        with open(output_path, 'a', encoding='utf-8') as output_file:
            output_file.write(
                f"Texto de la página {num_pagina + 1}:\n{texto_pagina}\n\n")

    doc.close()


# Ejemplo de uso
pdf_path = './pdf_folder/Circular25julio2023ReligionyAtencionEducativa.pdf'
output_path = './pdf_sinCabecera/Circular25julio2023ReligionyAtencionEducativa.pdf'
extraer_texto_sin_pie_de_pagina(pdf_path, output_path)
