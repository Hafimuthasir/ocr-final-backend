import io
import fitz
from PIL import Image
import os

def pdf_to_image(file):
    print("dddd",type(file))
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
            
    file_path = os.path.join('uploads', file.name)

    with open(file_path, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)

    pdf_data = fitz.open(file_path)

    pdf_data = fitz.open(file_path)
    page = pdf_data[0]  
    zoom_x = 2.0
    zoom_y = 2.0
    mat = fitz.Matrix(zoom_x, zoom_y)
    pix = page.get_pixmap(matrix=mat)
    return pix

