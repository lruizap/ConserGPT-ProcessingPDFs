import fitz  # PyMuPDF


def quitar_contenido_basura(pdf_path, output_path):
    # Abrir el archivo PDF
    pdf_document = fitz.open(pdf_path)

    # Crear un nuevo documento PDF vacío
    new_pdf_document = fitz.open()

    # Iterar sobre cada página del PDF original
    for page_number in range(pdf_document.page_count):
        # Obtener la página actual
        page = pdf_document[page_number]

        # Extraer texto de la página
        texto_pagina = page.get_text()

        # Aplicar lógica para quitar contenido basura (ajusta según tus necesidades)
        texto_filtrado = filtrar_contenido_basura(texto_pagina)

        # Agregar la página filtrada al nuevo documento PDF
        new_page = new_pdf_document.new_page(
            width=page.rect.width, height=page.rect.height)
        new_page.insert_text((10, 10), texto_filtrado)

    # Guardar el nuevo documento PDF
    new_pdf_document.save(output_path)

# Cerrar los documentos PDF
    pdf_document.close()
    new_pdf_document.close()


def filtrar_contenido_basura(texto):
    # Aquí puedes implementar la lógica específica para quitar contenido basura
    # Por ejemplo, eliminar palabras o patrones no deseados

    # En este ejemplo, simplemente devolvemos el texto sin cambios
    return texto


# Ruta del archivo PDF de entrada y salida
input_pdf_path = './pdf_folder/Circular25julio2023ReligionyAtencionEducativa.pdf'
output_pdf_path = './pdf_sinCabecera/Circular25julio2023ReligionyAtencionEducativa.pdf'

# Llamar a la función para quitar contenido basura
quitar_contenido_basura(input_pdf_path, output_pdf_path)
