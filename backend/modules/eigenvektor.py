import numpy as np

def calcEigenVector(matrix: np.ndarray, eigenValue: float) -> np.ndarray:
    """
    Calculate the eigen vector for a given eigen value.

    Parameters:
    matrix (np.ndarray): The square matrix.
    eigenValue (float): The eigen value.

    Returns:
    np.ndarray: The eigen vector corresponding to the given eigen value.
    """
    # A−λI Matrix
    A: np.ndarray = matrix - eigenValue * np.eye(matrix.shape[0])

    # Gaussian Elimination
    row: int
    col: int
    row, col = A.shape
    for i in range(min(row, col)):
        max_row: int = i + np.argmax(abs(A[i:, i]))
        A[[i, max_row]] = A[[max_row, i]] # Swap pivot rows to reduce floating-point error
        
        for j in range(i + 1, row):
            if A[j, i] != 0:
                factor: float = A[j, i] / A[i, i]
                A[j] -= factor * A[i]

    # Find Ax = 0, where x is the eigen vector
    x: np.ndarray = np.zeros(col)
    for i in range(col - 1, -1, -1):
        if abs(A[i, i]) > 1e-10:  # Avoid division by zero
            x[i] = -np.sum(A[i, i+1:] * x[i+1:]) / A[i, i]
        else:
            x[i] = 1  # Free variable (arbitrarily 1)

    print("Eigen vector (belum normalize): ", x)

    # Normalize the eigen vector
    eigenVector: np.ndarray = x / np.linalg.norm(x)
    return eigenVector


# Test Case Placeholder
matrix: np.ndarray = np.array([[4, 2], [1, 3]])
eigenValue: float = 5.0

eigenVector: np.ndarray = calcEigenVector(matrix, eigenValue)
print("Eigen vector:", eigenVector)