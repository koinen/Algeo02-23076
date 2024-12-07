from modules.image_processing import *
import PIL.Image as Image
import numpy as np

# image_now = Image.open("test.jpg")
# processed_image : Image.Image = ImageProcessing.makeImage(image_now)
# processed_image.show()

data : np.ndarray = np.load('uploads/dataset/image_data.npy')
print(data.shape)