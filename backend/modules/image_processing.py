import numpy as np
from PIL import Image

class ImageProcessing:
    def __init__(self):
        pass
    
    # def greyscaleToMatrix(self, image: Image.Image):
    #     # Convert the image to greyscale
    #     image : Image.Image = image.convert("RGB")
    #     image_array : np.ndarray = np.array(image)
    #     greyscaledImageMatrix : np.ndarray = np.zeros((len(image_array), len(image_array[0])), dtype=int)
    #     for i in range(len(image_array)):
    #         for j in range(len(image_array[0])):
    #             # Convert to greyscale
    #             greyscaledImageMatrix[i][j] = 0.2989 * image_array[i][j][0] + 0.5870 * image_array[i][j][1] + 0.1140 * image_array[i][j][2]
    #     return greyscaledImageMatrix

    # @staticmethod
    # def flatten_index(x, y, size):
    #     """Helper function to flatten (x, y) coordinates into a 1D index."""
    #     return x + (y * size)  # Row-major order flattening

    def resizeAndGreyscale(self, image: Image.Image):
        image : Image.Image = image.convert("L") # Convert the image to greyscale
        image = image.resize((100, 100)) # Resize the image to 100x100

        # Resize by bicubic interpolation
        
        # bicubicMatrix = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                           [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                           [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        #                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        #                           [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                           [0, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                           [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        #                           [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
        #                           [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                           [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        #                           [0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0],
        #                           [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
        #                           [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                           [0, 0, 0, 0, 0, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0],
        #                           [0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0],
        #                           [0, 0, 0, 0, 0, 1, 2, 3, 0, 2, 4, 6, 0, 3, 6, 9]])
        
        # Generate Image Bicubic Matrix
        # I_SIZE = 4  # 4x4 grid for I(x, y)
        # F_SIZE = 2  # 2x2 grid for f(x, y)
        # VECTOR_LENGTH = 16  # Total number of entries in the flattened vectors
        # D = np.zeros((VECTOR_LENGTH, VECTOR_LENGTH))  # Transition matrix

        # # Loop over the smaller 2x2 grid for f(x, y) and its derivatives
        # for n in range(4):
        #     for x in range(2):
        #         for y in range(2):
        #             if n == 0:
        #                 D[self.flatten_index(x, y, F_SIZE)][self.flatten_index(x + 1, y + 1, I_SIZE)] += 1
        #             elif n == 1:
        #                 D[4 * n + self.flatten_index(x, y, F_SIZE)][self.flatten_index(x + 1, y + 2, I_SIZE)] = 0.5
        #                 D[4 * n + self.flatten_index(x, y, F_SIZE)][self.flatten_index(x, y + 1, I_SIZE)] = -0.5
        #             elif n == 2:
        #                 D[4 * n + self.flatten_index(x, y, F_SIZE)][self.flatten_index(x + 1, y + 2, I_SIZE)] += 0.5
        #                 D[4 * n + self.flatten_index(x, y, F_SIZE)][self.flatten_index(x + 1, y, I_SIZE)] += -0.5
        #             else:
        #                 D[4 * n + self.flatten_index(x, y, F_SIZE)][self.flatten_index(x + 2, y + 2, I_SIZE)] += 0.25
        #                 D[4 * n + self.flatten_index(x, y, F_SIZE)][self.flatten_index(x, y + 1, I_SIZE)] += -0.25
        #                 D[4 * n + self.flatten_index(x, y, F_SIZE)][self.flatten_index(x + 1, y, I_SIZE)] += -0.25
        #                 D[4 * n + self.flatten_index(x, y, F_SIZE)][self.flatten_index(x + 1, y + 1, I_SIZE)] += -0.25

        

    def flatten(self, resized):
        # Flatten the image
        height : int = len(resized)
        width : int = len(resized[0])
        flattened : np.ndarray = np.zeros(height * width, dtype=int)
        for i in range(height):
            for j in range(width):
                flattened[i * height + j] = resized[i][j]

        return flattened
