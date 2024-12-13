from image_processing import ImageProcessing
from general_processing import GeneralProcessing
from PIL import Image
import numpy as np
import os

def processDatabaseImage(dataset_file, reduced_dimension):
    dataset = np.load(f"../uploads/dataset/{dataset_file}")
    print("Dataset loaded:", dataset[0])
    center_dataset = GeneralProcessing.centerMatrix(dataset)
    print("Centered dataset:", center_dataset[0])
    mean = GeneralProcessing.meansMatrix(dataset)
    print("Mean matrix:", mean)
    u, s, vh = np.linalg.svd(center_dataset)
    project_dataset = center_dataset @ vh.T[:, :reduced_dimension]
    print("Projected dataset:", project_dataset[0])
    
    # Save necessary variables for later use
    np.save("../uploads/processed/mean_img.npy", mean)
    np.save("../uploads/processed/project_dataset_img.npy", project_dataset)
    np.save("../uploads/processed/vh_img.npy", vh.T[:, :reduced_dimension])
    
    return mean, project_dataset, vh.T[:, :reduced_dimension]

def openProcessedDatabaseImage():
    if not os.path.exists("../uploads/processed/mean_img.npy"):
        return None, None, None
    mean = np.load("../uploads/processed/mean_img.npy")
    project_dataset = np.load("../uploads/processed/project_dataset_img.npy")
    pca = np.load("../uploads/processed/vh_img.npy")
    return mean, project_dataset, pca

def processQueryImage(image_file_name, mean, pca):
    image_query = Image.open(f"../uploads/{image_file_name}")
    image_query = ImageProcessing.processImage(image_query)
    print("Processed query image:", image_query)
    image_query = image_query - mean
    print("Centered query image:", image_query)
    project_query = image_query @ pca
    print("Projected query image:", project_query)
    return project_query

def queryImage(image_file_name, mean, pca):
    project_query = processQueryImage(image_file_name, mean, pca)
    project_dataset = np.load("../uploads/processed/project_dataset.npy")
    index = GeneralProcessing.euclideanClosest(project_dataset, project_query)
    with open("../uploads/dataset/image_file_names.txt", "r") as f:
        lines = f.readlines()
        file_names = [line.strip() for line in lines]
    
    top_5_files = [file_names[i] for i in index[:5]]
    return top_5_files
    





