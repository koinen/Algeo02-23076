from modules.image_processing import *
import PIL.Image as Image

image_now = Image.open("test.jpg")
processed_image : Image.Image = ImageProcessing.makeImage(image_now)
processed_image.show()