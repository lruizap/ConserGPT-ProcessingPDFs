import os
import PyPDF2


def quitar_cabecera_pie(pdf_path, output_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            media_box = page.mediabox
            page_width = media_box.width
            page_height = media_box.height

            # Puedes ajustar estos valores según tus necesidades
            margin_top = 105
            margin_bottom = 50

            # Eliminar cabecera
            media_box.lower_left = (0, margin_bottom)
            media_box.upper_right = (page_width, page_height)

            # Eliminar pie de página
            media_box.lower_left = (0, 0)
            media_box.upper_right = (page_width, page_height - margin_top)

            pdf_writer.add_page(page)

        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)


def pdf_a_texto(pdf_path, output_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(text)


# Ejemplo de uso
pdf_path = './pdf_folder/Circular25julio2023ReligionyAtencionEducativa.pdf'
output_path_sin_cabecera_pie = './pdf_sinCabecera/Circular25julio2023ReligionyAtencionEducativa.pdf'
output_path_texto_plano = './salida/Circular25julio2023ReligionyAtencionEducativa.txt'

quitar_cabecera_pie(pdf_path, output_path_sin_cabecera_pie)
pdf_a_texto(output_path_sin_cabecera_pie, output_path_texto_plano)
