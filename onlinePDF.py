import cv2
from langchain_community.document_loaders import OnlinePDFLoader

loader = OnlinePDFLoader(
    "https://www.suneo.mx/literatura/subidas/Miguel%20de%20Cervantes%20El%20Ingenioso%20Hidalgo%20Don%20Quijote%20de%20la%20Mancha.pdf")
document = loader.load()

print(document)

#!######################################

# from urllib.request import Request, urlopen
# from PyPDF2 import PdfWriter, PdfReader
# from io import StringIO

# url = "https://www.adideandalucia.es/normas/ordenes/Orden15abril2011SubvencionesAsociaciones.pdf"
# writer = PdfWriter()

# remoteFile = urlopen(Request(url)).read()
# memoryFile = StringIO(remoteFile)
# pdfFile = PdfReader(memoryFile)

# for pageNum in range(pdfFile.getNumPages()):
#     currentPage = pdfFile.getPage(pageNum)
#     # currentPage.mergePage(watermark.getPage(0))
#     writer.addPage(currentPage)


# outputStream = open("output.pdf", "wb")
# writer.write(outputStream)
# outputStream.close()

#!######################################
