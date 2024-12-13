from image_recognition import queryImage
from general_processing import GeneralProcessing
from image_processing import ImageProcessing
from PIL import Image
import numpy as np



def testGeneralProcessing(dataset, query, mean):
    # meanDataset = GeneralProcessing.meanMatrix(dataset)
    pca = GeneralProcessing.principalComponent(dataset, 1000)
    projectedDataset = GeneralProcessing.projectedDataset(dataset, 1000)
    for i in range(query.shape[0]):
        queryMean = query[i] - mean[0][i]
    projectedQuery = GeneralProcessing.projectMatrix(queryMean, pca, 1000)
    top = 10
    closest = []
    for i in range(projectedDataset.shape[0]):
        distance = GeneralProcessing.euclideanDistance(projectedQuery, projectedDataset[i])
        closest.append((distance, i))
    closest = sorted(closest)
    index = []
    for i in range(len(closest)):
        index.append(closest[i][1])
    print(index[:top])
    return index[:top]

def processDatabase(dataset_file, reduced_dimension):
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
    np.save("../uploads/processed/mean.npy", mean)
    np.save("../uploads/processed/project_dataset.npy", project_dataset)
    np.save("../uploads/processed/vh.npy", vh.T[:, :reduced_dimension])
    
    return mean, project_dataset, vh.T[:, :reduced_dimension]

def openProcessedDatabase():
    mean = np.load("../uploads/processed/mean.npy")
    project_dataset = np.load("../uploads/processed/project_dataset.npy")
    pca = np.load("../uploads/processed/vh.npy")
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

if __name__ == "__main__":
    # # Process the database
    # processDatabase("image_data.npy", 50)
    # # Open the processed database
    mean, project_dataset, vh = openProcessedDatabase()
    # # Process the query image
    index = queryImage("aa.png", mean, vh)
    print(index)
    # dataset = np.load("../uploads/dataset/image_data.npy")
    # print("Dataset loaded:", dataset[0])
    # center_dataset = GeneralProcessing.centerMatrix(dataset)
    # print("Centered dataset:", center_dataset[0])
    # mean = GeneralProcessing.meansMatrix(dataset)
    # print("Mean matrix:", mean)
    # u, s, vh = np.linalg.svd(center_dataset)
    # reduced_dimension = 50
    # project_dataset = center_dataset @ vh.T[:, :reduced_dimension]
    # print("Projected dataset:", project_dataset[0])


    # # Process the query image
    # image_query = Image.open("../uploads/aa.png")
    # image_query = ImageProcessing.processImage(image_query)
    # print("Processed query image:", image_query)
    # image_query = image_query - mean
    # print("Centered query image:", image_query)
    # project_query = image_query @ vh.T[:, :reduced_dimension]
    # print("Projected query image:", project_query)

    # if project_query.all() == processQueryImage("aa.png", mean, vh, reduced_dimension).all():
    #     print("Query image processed correctly")



    # Example usage
    # project_query = processQueryImage("aa.png", mean, vh, reduced_dimension)
    # Find the closest match

    # # index = testGeneralProcessing(dataset, image_query, mean)
    # project_dataset = GeneralProcessing.projectPCdatabase(center_dataset, pca, 50)
    # print(project_dataset[0])
    # queryw = GeneralProcessing.projectPCquery(image_query, pca, 50)
    # print(queryw)
    # index = GeneralProcessing.euclideanClosest(project_dataset, queryw)
    # index2 = GeneralProcessing.cosineClosest(project_dataset, queryw)
    # print(pca)
    # print(mean)
    # print(project_dataset)
    # print(queryw)
    # print(index)
    # print(index2)




    