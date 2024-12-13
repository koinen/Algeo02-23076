import numpy as np
from PIL import Image

class ImageProcessing:
    def __init__(self):
        pass

    @staticmethod
    def __convertImageToMatrix(image: Image.Image) -> np.ndarray:
        """
        Convert an image to a 3D matrix (RGB).
        """
        image = image.convert("RGB")
        imageMatrix : np.ndarray = np.array(image)
        return imageMatrix
    
    @staticmethod
    def __greyscale(imageMatrix: np.ndarray) -> np.ndarray:
        # Convert the image to greyscale
        image = Image.fromarray(imageMatrix)
        greyscaled = image.convert("L")
        return np.array(greyscaled)
        # greyscaledImageMatrix : np.ndarray = np.zeros((len(imageMatrix), len(imageMatrix[0])), dtype=int)
        # for i in range(len(imageMatrix)):
        #     for j in range(len(imageMatrix[0])):
        #         # Convert to greyscale
        #         greyscaledImageMatrix[i][j] = int(0.2989 * imageMatrix[i][j][0] + # Red
        #                                           0.5870 * imageMatrix[i][j][1] + # Green
        #                                           0.1140 * imageMatrix[i][j][2])  # Blue
        # return greyscaledImageMatrix.astype(np.uint8)

    @staticmethod
    def __flatten_index(x, y, size):
        """Helper function to flatten (x, y) coordinates into a 1D index."""
        return x + (y * size)  # Row-major order flattening
    
    @staticmethod
    def __getCoef(surroundings: np.ndarray) -> np.ndarray:
        bicubicMatrix : np.ndarray = np.array( [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                                                [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
                                                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0],
                                                [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
                                                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0],
                                                [0, 0, 0, 0, 0, 1, 2, 3, 0, 2, 4, 6, 0, 3, 6, 9]])
        invertedBicubicMatrix : np.ndarray = np.linalg.inv(bicubicMatrix)
        coef : np.ndarray = np.dot(invertedBicubicMatrix, surroundings)
        return coef

    @staticmethod
    def __getInterpolatedValue(coef: np.ndarray, x: float, y: float) -> float:
        result : float = 0.
        for i in range(16):
            result += coef[i] * (x ** (i % 4)) * (y ** (i // 4))
        return int(result)

    @staticmethod 
    def __generateDMatrix() -> np.ndarray:
        # Generate Image Bicubic Matrix
        I_SIZE = 4  # 4x4 grid for I(x, y)
        F_SIZE = 2  # 2x2 grid for f(x, y)
        D = np.zeros((16, 16))  # Transition matrix

        # Loop over the smaller 2x2 grid for f(x, y) and its derivatives
        for n in range(4):
            for x in range(2):
                for y in range(2):
                    if n == 0:
                        D[ImageProcessing.__flatten_index(x, y, F_SIZE)][ImageProcessing.__flatten_index(x + 1, y + 1, I_SIZE)] += 1
                    elif n == 1:
                        D[4 * n + ImageProcessing.__flatten_index(x, y, F_SIZE)][ImageProcessing.__flatten_index(x + 1, y + 2, I_SIZE)] = 0.5
                        D[4 * n + ImageProcessing.__flatten_index(x, y, F_SIZE)][ImageProcessing.__flatten_index(x, y + 1, I_SIZE)] = -0.5
                    elif n == 2:
                        D[4 * n + ImageProcessing.__flatten_index(x, y, F_SIZE)][ImageProcessing.__flatten_index(x + 1, y + 2, I_SIZE)] += 0.5
                        D[4 * n + ImageProcessing.__flatten_index(x, y, F_SIZE)][ImageProcessing.__flatten_index(x + 1, y, I_SIZE)] += -0.5
                    else:
                        D[4 * n + ImageProcessing.__flatten_index(x, y, F_SIZE)][ImageProcessing.__flatten_index(x + 2, y + 2, I_SIZE)] += 0.25
                        D[4 * n + ImageProcessing.__flatten_index(x, y, F_SIZE)][ImageProcessing.__flatten_index(x, y + 1, I_SIZE)] += -0.25
                        D[4 * n + ImageProcessing.__flatten_index(x, y, F_SIZE)][ImageProcessing.__flatten_index(x + 1, y, I_SIZE)] += -0.25
                        D[4 * n + ImageProcessing.__flatten_index(x, y, F_SIZE)][ImageProcessing.__flatten_index(x + 1, y + 1, I_SIZE)] += -0.25    
        return D

    @staticmethod
    def __resize(greyscaledImageMatrix: np.ndarray) -> np.ndarray:
        
        """
        Resize the image using bicubic interpolation.
        """
        image = Image.fromarray(greyscaledImageMatrix)
        resized = image.resize((100, 100), Image.BICUBIC)
        return np.array(resized)
        # IMAGE_SIZE = 200
        # resized : np.ndarray = np.zeros((IMAGE_SIZE, IMAGE_SIZE), dtype=int)
        # width : int = len(greyscaledImageMatrix[0])
        # height : int = len(greyscaledImageMatrix)
        # heightScale : float = IMAGE_SIZE / height
        # widthScale : float = IMAGE_SIZE / width
        # downWidthScale : int = max(1, int(1 / widthScale)) 
        # downHeightScale : int = max(1, int(1 / heightScale))
        # D = ImageProcessing.__generateDMatrix()
        # for x in range(0, width, downWidthScale):
        #     for y in range(0, height, downHeightScale):
        #         # Get the surrounding 4x4 grid
        #         surroundings : np.ndarray = np.zeros(16)
        #         for i in range(4):
        #             for j in range(4):
        #                 oldX = max(min(x + i - 1, width - 1), 0)
        #                 oldY = max(min(y + j - 1, height - 1), 0)
        #                 surroundings[4 * i + j] = greyscaledImageMatrix[oldY][oldX]
        #         coef : np.ndarray = ImageProcessing.__getCoef(np.dot(D, surroundings))
        #         for i in range(0, int(heightScale) + 1):
        #             for j in range(0, int(widthScale) + 1):
        #                 newValue : int = ImageProcessing.__getInterpolatedValue(coef, i / heightScale, j / widthScale)
        #                 newValue = max(0, min(newValue, 255))
        #                 newRow : int = min(int(y * heightScale + i), IMAGE_SIZE-1)
        #                 newCol : int = min(int(x * widthScale + j), IMAGE_SIZE-1)
        #                 resized[newRow][newCol] = newValue
        
        # return resized.astype(np.uint8)

    @staticmethod
    def __flatten(resized : np.ndarray) -> np.ndarray:
        """
        Flatten the resized image to a vector (1D Matrix).
        """
        flattened : np.ndarray = np.array(resized).flatten()
        # height : int = len(resized)
        # width : int = len(resized[0])
        # flattened : np.ndarray = np.zeros(height * width, dtype=int)
        # for i in range(height):
        #     for j in range(width):
        #         flattened[i * height + j] = resized[i][j]

        return flattened
    
    @staticmethod
    def makeImage(image: Image.Image) -> Image.Image:
        res : np.ndarray = ImageProcessing.__resize(ImageProcessing.__greyscale(ImageProcessing.__convertImageToMatrix(image)))
        return Image.fromarray(res)

    @staticmethod
    def processImage(image: Image.Image) -> np.ndarray:
        """
        Process the image to a 1D matrix.
        """
        res : np.ndarray = ImageProcessing.__flatten(ImageProcessing.__resize(ImageProcessing.__greyscale(ImageProcessing.__convertImageToMatrix(image))))
        return res
    
    @staticmethod
    def euclideanDistance(image1: np.ndarray, image2: np.ndarray) -> float:
        """
        Calculate the Euclidean distance between two images.
        """
        return np.linalg.norm(image1 - image2)
