from image_processing import ImageProcessing
from general_processing import GeneralProcessing
import zipfile
from PIL import Image
import os
import numpy as np
from typing import Tuple, List

def ziptoDataset(path: str) -> np.ndarray:
    # Ensure the path exists
    if not os.path.exists(path):
        raise Exception("Path does not exist")
    
    image_list: List[np.ndarray] = []
    with zipfile.ZipFile(path, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            try:
                with zip_ref.open(file_name) as file:
                    image: Image = Image.open(file)
                    image_processed: np.ndarray = ImageProcessing.processImage(image)
                    image_list.append(image_processed)
            except Exception as e:
                print(f"Error processing image {file_name}: {str(e)}")
    dataset: np.ndarray = np.array(image_list)
    return dataset

def principalComponent(dataset: np.ndarray, kval: int) -> np.ndarray:
    if kval == -1:
        kval = dataset.shape[1]
    centeredMatrix: np.ndarray = GeneralProcessing.centerMatrix(dataset)
    covMatrix: np.ndarray = GeneralProcessing.covarianceMatrix(centeredMatrix)
    eigenValues: np.ndarray = GeneralProcessing.eigenValues(covMatrix, 100)
    eigenSpace: np.ndarray = GeneralProcessing.eigenSpace(eigenValues, covMatrix)
    return eigenSpace[:, :kval]

def projectedDataset(imageMatrix: np.ndarray, kval: int) -> np.ndarray:
    if kval == -1:
        kval = imageMatrix.shape[1]
    eigenSpace: np.ndarray = principalComponent(imageMatrix, kval)
    projectedImages = []
    for i in range(imageMatrix.shape[0]):
        projectedImage: np.ndarray = GeneralProcessing.projectMatrix(imageMatrix[i], eigenSpace, kval)
        projectedImages.append(projectedImage)
    return np.array(projectedImages)

def queryImage(image: Image, dataset: np.ndarray, projectedDataset: np.ndarray, kval: int) -> np.ndarray:
    if kval == -1:
        kval = dataset.shape[1]
    imageMatrix: np.ndarray = ImageProcessing.processImage(image)
    meanDataset: np.ndarray = GeneralProcessing.meanMatrix(dataset) #an array of means
    centeredImage: np.ndarray = imageMatrix - meanDataset
    principalComponents: np.ndarray = principalComponent(dataset, kval)
    projectedImage: np.ndarray = GeneralProcessing.projectMatrix(centeredImage, principalComponents, kval)
    top: int = 5
    closest = []
    for i in range(projectedDataset.shape[0]):
        distance: float = GeneralProcessing.euclideanDistance(projectedImage, projectedDataset[i])
        closest.append(distance)
    
    closest = sorted(closest, reverse=True)
    closest = closest[:top]
    return np.array(closest)

    





