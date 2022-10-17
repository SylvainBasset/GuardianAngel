from PIL import Image
from pytesseract import pytesseract


#---------------------------------------------------------------------------#
if __name__ == "__main__" :
   print("heyhey")

                                       # Define path to image
   path_to_image = 'test.png'
                                       # Point tessaract_cmd to tessaract.exe
   pytesseract.tesseract_cmd = r'tesseract'
                                       # Open image with PIL
   img = Image.open(path_to_image)
                                       # Extract text from image
   text = pytesseract.image_to_string(img)
   print(text)