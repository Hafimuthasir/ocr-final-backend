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

    pdf_file = fitz.open(file_path)



    pdf_data = fitz.open(file_path)

    pdf_data = fitz.open(file_path)
    page = pdf_data[0]  # get the specified page
    zoom_x = 2.0
    zoom_y = 2.0
    mat = fitz.Matrix(zoom_x, zoom_y)
    pix = page.get_pixmap(matrix=mat)
    # pix = page.get_pixmap()  #
    return pix





    # pdf = PyMuPDF.PDF(pdf_data)

    # Convert the first page of the PDF to a PIL Image object
    # page = pdf[0]
    # image = page.getImage(alpha=False)

    # Convert the PIL Image object to a byte stream
    # image_bytes = io.BytesIO()
    # image.save(image_bytes, format='PNG')
    # image_bytes.seek(0)