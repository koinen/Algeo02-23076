import numpy as np
from typing import Tuple

class GeneralProcessing:
    def __init__(self):
        pass

    def matrixCovariance(Matrix: np.ndarray) -> np.ndarray:
        """
        Calculate the covariance matrix of a given matrix.
        """
        covarianceMatrix: np.ndarray = np.cov(Matrix)
        return covarianceMatrix
    
    def matrixFlatten(Matrix: np.ndarray) -> np.array:
        """
        Flatten a given matrix.
        """
        flatMatrix: np.array = Matrix.flatten()

        return flatMatrix

    
    def matrixMean(Matrix: np.ndarray) -> np.array:
        """
        Calculate the mean of a given matrix.
        """
        nData: int = Matrix.shape[0]
        nFeatures: int = Matrix.shape[1]
        meanMatrix: np.ndarray = np.zeros(nFeatures)
        for i in range(nFeatures):
            meanFeature: float = 0
            for j in range(nData):
                meanFeature += Matrix[j][i]
            meanFeature /= nData
            meanMatrix[i] = meanFeature
        return meanMatrix
    
    def matrixStandard(Matrix: np.ndarray) -> np.ndarray:
        """
        Center a given matrix.
        """
        meanMatrix: np.ndarray = GeneralProcessing.matrixMean(Matrix)
        centeredMatrix: np.ndarray = Matrix
        nData: int = Matrix.shape[0]
        nFeatures: int = Matrix.shape[1]
        for i in range(nFeatures):
            for j in range(nData):
                centeredMatrix[j][i] -= meanMatrix[i]
        
        return centeredMatrix
    
    def arrayStandard(Array: np.array, meanMatrix: np.ndarray) -> np.array:
        """
        Center a given array.
        """

        meanArray: np.array = np.zeros(meanMatrix.shape[1])
        for i in range(meanMatrix.shape[1]):
            meanArray[i] = meanMatrix[0][i]
        centeredArray: np.array = Array - meanArray
        return centeredArray
    
    def euclideanDistance(Array1: np.array, Array2: np.array) -> float:
        """
        Calculate the euclidean distance between two arrays.
        """
        distance: float = 0
        for i in range(Array1.shape[0]):
            distance += (Array1[i] - Array2[i])**2
        return np.sqrt(distance)
    
    def cosineSimilarity(Array1: np.array, Array2: np.array) -> float:
        """
        Calculate the cosine similarity between two arrays.
        """
        dotProduct: float = np.dot(Array1, Array2)
        normArray1: float = np.linalg.norm(Array1)
        normArray2: float = np.linalg.norm(Array2)
        return dotProduct / (normArray1 * normArray2)


    def SingularValueDecomposition(Matrix: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate the singular value decomposition of a given matrix.
        """
        U, S, V = np.linalg.svd(Matrix)
        return U, S, V

    def mainComponent(Matrix: np.ndarray, nComponents: int) -> np.ndarray:
        """
        Calculate the main components of a given matrix.
        """
        U, S, V = GeneralProcessing.SingularValueDecomposition(Matrix)
        mainComponents: np.ndarray = U[:, :nComponents]
        return mainComponents

    def matrixProjection(Matrix: np.array, mainComponents: np.ndarray) -> np.ndarray:
        """
        Project a given matrix into the main components.
        """
        projectionMatrix: np.ndarray = np.dot(Matrix, mainComponents)
        return projectionMatrix

    def arrayProjection(Array: np.array, mainComponents: np.ndarray) -> np.array:
        """
        Project a given array into the main components.
        """
        projectionArray: np.array = np.dot(Array, mainComponents)
        return projectionArray

    def principalComponentAnalysis(Matrix: np.ndarray, nComponents: int) -> np.ndarray:
        """
        Perform principal component analysis on a given matrix.
        """
        centeredMatrix: np.ndarray = GeneralProcessing.matrixStandard(Matrix)
        mainComponents: np.ndarray = GeneralProcessing.mainComponent(centeredMatrix, nComponents)
        return mainComponents
    
    def arrayZScore(Array: np.array, meanMatrix: np.ndarray, stdMatrix: np.ndarray) -> np.array:
        """
        Calculate the Z-score of a given array.
        """
        zScoreArray: np.array = np.zeros(Array.shape[0])
        for i in range(Array.shape[0]):
            zScoreArray[i] = (Array[i] - meanMatrix[i]) / stdMatrix[i]
        return zScoreArray
    


    
