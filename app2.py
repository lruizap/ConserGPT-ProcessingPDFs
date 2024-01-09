import fitz  # PyMuPDF


def cortar_pdf_desde_anexo(archivo_pdf, palabra_clave="ANEXO"):
    doc = fitz.open(archivo_pdf)

    # Buscar la página que contiene la palabra clave "ANEXO"
    indice_anexo = None
    for num_pagina in range(doc.page_count):
        pagina = doc[num_pagina]
        texto_pagina = pagina.get_text()

        if palabra_clave in texto_pagina:
            indice_anexo = num_pagina
            break

    if indice_anexo is not None:
        # Guardar las páginas antes del anexo
        doc_antes_anexo = fitz.open()
        doc_antes_anexo.insert_pdf(doc, from_page=0, to_page=indice_anexo-1)
        doc_antes_anexo.save(f"pdf_antes_anexo.pdf")
        doc_antes_anexo.close()

    doc.close()


# Ejemplo de uso
archivo_pdf = "./pdf_folder/Instruccion26septiembre2023PremiosExtraordinariosMusica.pdf"
cortar_pdf_desde_anexo(archivo_pdf)
