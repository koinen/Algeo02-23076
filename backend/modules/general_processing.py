import numpy as np
import math
from typing import Tuple, List
from eigenvektor import calcEigenVector

# ALLOWED NDARRAY PRIMITIVES : transpose, multiply

class GeneralProcessing:
    def __init__(self):
        pass

    @staticmethod
    def multiplyMatrix(matrix1: np.ndarray, matrix2: np.ndarray) -> np.ndarray:
        multMatrix: np.ndarray = np.zeros((matrix1.shape[0], matrix2.shape[1]))
        for i in range(matrix1.shape[0]):
            for j in range(matrix2.shape[1]):
                for k in range(matrix1.shape[1]):
                    multMatrix[i][j] += matrix1[i][k] * matrix2[k][j]

        return multMatrix

    @staticmethod
    def transpose(matrix: np.ndarray) -> np.ndarray:
        transposedMatrix: np.ndarray = np.zeros((matrix.shape[1], matrix.shape[0]))
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                transposedMatrix[j][i] = matrix[i][j]
        return transposedMatrix

    @staticmethod
    def flattenMatrix(matrix: np.ndarray) -> np.ndarray:
        len: int = matrix.shape[0] * matrix.shape[1]
        flatArray: np.ndarray = np.zeros(len)
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                flatArray[i * matrix.shape[1] + j] = matrix[i][j]
        return flatArray
    
    @staticmethod
    def meanMatrix(matrix: np.ndarray) -> np.ndarray:
        nSamples: int = matrix.shape[0]
        nFeatures: int = matrix.shape[1]
        meanMatrix: np.ndarray = np.zeros(nFeatures)
        sum: float = 0
        for i in range(nFeatures):
            for j in range(nSamples):
                sum += matrix[j][i]
            meanMatrix[i] = sum / nSamples
        return meanMatrix
    
    @staticmethod
    def centerMatrix(matrix: np.ndarray) -> np.ndarray:
        mean: np.ndarray = GeneralProcessing.meanMatrix(matrix)
        centeredMatrix: np.ndarray = np.zeros(matrix.shape)
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                centeredMatrix[i][j] = matrix[i][j] - mean[j]
        return centeredMatrix
    
    @staticmethod
    def covarianceMatrix(matrix: np.ndarray) -> np.ndarray:
        nSamples: int = matrix.shape[0]
        covMatrix: np.ndarray = 1/nSamples * GeneralProcessing.multiplyMatrix(GeneralProcessing.transpose(matrix), matrix)
        return covMatrix
    
    @staticmethod
    def absVector(vector: np.ndarray) -> float:
        sum: float = 0
        for i in range(vector.shape[0]):
            sum += vector[i] ** 2
        return math.sqrt(sum)
    
    @staticmethod
    def normalizeVector(vector: np.ndarray) -> np.ndarray:
        abs: float = GeneralProcessing.absVector(vector)
        return vector / abs

    @staticmethod
    def qrDecomposition(matrix: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        n: int = matrix.shape[0]
        q: np.ndarray = np.zeros((n, n))
        r: np.ndarray = np.zeros((n, n))
        for j in range(n):
            v: np.ndarray = matrix[:, j]
            for i in range(j):
                dot: int = np.dot(q[:, i], matrix[:, j])
                v = v - dot * q[:, i]
            q[:, j] = GeneralProcessing.normalizeVector(v)
        r = GeneralProcessing.multiplyMatrix(GeneralProcessing.transpose(q), matrix)
        return q, r
    
    @staticmethod
    def isUpperTriangular(matrix: np.ndarray) -> bool:
        for i in range(matrix.shape[0]):
            for j in range(i):
                if abs(matrix[i][j]) > 1e-10: #tolerance, basically 0
                    return False
        return True
    
    @staticmethod
    def qrLoop(matrix: np.ndarray, nIter: int) -> np.ndarray:
        q: np.ndarray = matrix
        for i in range(nIter):
            q, r = GeneralProcessing.qrDecomposition(q)
            q = GeneralProcessing.multiplyMatrix(r, q)
            if GeneralProcessing.isUpperTriangular(q):
                break
        return q
    
    @staticmethod
    def eigenValues(matrix: np.ndarray, nIter: int) -> np.ndarray:
        q: np.ndarray = GeneralProcessing.qrLoop(matrix, nIter)
        eigenValues: np.ndarray = np.zeros(matrix.shape[0])
        for i in range(matrix.shape[0]):
            eigenValues[i] = q[i][i]
        
        eigenValues = np.sort(eigenValues)[::-1]
        
        return eigenValues
    
    @staticmethod
    def eigenSpace(eigenValues: np.ndarray, matrix: np.ndarray) -> np.ndarray:
        eigenSpace: List[np.ndarray] = []
        for i in range(eigenValues.shape[0]):
            eigenVector: np.ndarray = calcEigenVector(matrix, eigenValues[i])
            eigenSpace.append(eigenVector)
        eigenSpace = np.array(eigenSpace)
        eigenSpace = GeneralProcessing.transpose(eigenSpace)
        return eigenSpace
    
    @staticmethod
    def projectMatrix(matrix: np.ndarray, eigenSpace: np.ndarray, kval: int) -> np.ndarray:
        simplifiedEigenSpace: np.ndarray = eigenSpace[:, :kval]
        projectedMatrix: np.ndarray = GeneralProcessing.multiplyMatrix(matrix, simplifiedEigenSpace)
        return projectedMatrix
    
    @staticmethod
    def euclideanDistance(vector1: np.ndarray, vector2: np.ndarray) -> float:
        sum: float = 0
        for i in range(vector1.shape[0]):
            sum += (vector1[i] - vector2[i]) ** 2
        return math.sqrt(sum)

    
