# from langchain.document_loaders import OnlinePDFLoader
import cv2
from langchain_community.document_loaders import OnlinePDFLoader

loader = OnlinePDFLoader(
    "https://www.suneo.mx/literatura/subidas/Miguel%20de%20Cervantes%20El%20Ingenioso%20Hidalgo%20Don%20Quijote%20de%20la%20Mancha.pdf")
document = loader.load()

print(document)
