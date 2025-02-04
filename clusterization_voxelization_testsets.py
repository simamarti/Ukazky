import re
from math import floor, ceil, inf
import os
from glob import glob
import shutil

def bbox(data : str) -> None:
    
    x_min = inf; x_max = -inf; y_min = inf; y_max = -inf; z_min = inf; z_max = -inf    
    with open(data, 'r') as f:
        for line in f:
            splitted = re.split(' |\t', line)
            x_min = min(x_min, float(splitted[0])); x_max = max(x_max, float(splitted[0]))
            y_min = min(y_min, float(splitted[1])); y_max = max(y_max, float(splitted[1]))
            z_min = min(z_min, float(splitted[2])); z_max = max(z_max, float(splitted[2]))
    
    return [floor(x_min), ceil(x_max), floor(y_min), ceil(y_max), floor(z_min), ceil(z_max)]

def makeCube(size : int, x_min : float, x_max : float, y_min : float, y_max : float, z_min : float, z_max : float) -> list[int]:
    
    
        
    x_range = x_max - x_min; y_range = y_max - y_min; z_range = z_max - z_min
    edge = max(x_range, y_range, z_range)
    
    edge = size*ceil(edge/size)
    
    x_diff = edge - x_range; y_diff = edge - y_range; z_diff = edge - z_range
    if x_diff%2:
        x_min -= ceil(x_diff/2);x_max += floor(x_diff/2)
    else:
        x_min -= x_diff/2; x_max += x_diff/2
    if y_diff%2:
        y_min -= ceil(y_diff/2);y_max += floor(y_diff/2)
    else:
        y_min -= y_diff/2; y_max += y_diff/2
                
    z_max += z_diff
    return [x_min, x_max, y_min, y_max, z_min, z_max]

def stream2Array(data):
    result = []
    
    with open(data, 'r', encoding = 'utf-8') as f:
        data = f.readlines()
        
    for line in data:
        splitted = re.split('   |  |\t\t| |\t', line)
        if len(splitted) >= 3:
            result.append([float(splitted[0]), float(splitted[1]), float(splitted[2].strip())])

    return result

def normCoords(data, x_min, x_max, y_min, y_max, z_min, z_max):
    normalized = []

    for point in data:
        x_n = (point[0] - x_min)/(x_max - x_min)
        y_n = (point[1] - y_min)/(y_max - y_min)
        z_n = (point[2] - z_min)/(z_max - z_min)
        
        normalized.append([x_n, y_n, z_n])
    
    return normalized
    
def hashTable(data, n_r):
    c = 0.99
    H = {}; J = {}

    for idx, point in enumerate(data):
        x = point[0]; y = point[1]; z = point[2]
        
        x_j = ceil(c*n_r*x)
        y_j = ceil(c*n_r*y)
        z_j = ceil(c*n_r*z)
        
        h = x_j + y_j*n_r + z_j*n_r*n_r
        
        if not h in H:
            H[h] = []
        H[h].append(idx)
        
        J[idx] = h
    
    return H, J
    
def centroid(data, voxel):
    x_sum = 0; y_sum = 0; z_sum = 0
    
    for pt in voxel:
        x_sum += data[pt][0]
        y_sum += data[pt][1]
        z_sum += data[pt][2]
    
    n = len(voxel)
    return x_sum/n, y_sum/n, z_sum/n
   
def voxelization(input, size, idx):
    
    # Create bounding box for point cloud
    x_min, x_max, y_min, y_max, z_min, z_max = bbox(input)

    # Make cube for voxelization, size of edge is power of inserted size of voxle
    x_min, x_max, y_min, y_max, z_min, z_max = makeCube(size, x_min, x_max, y_min, y_max, z_min, z_max)

    dataArray = stream2Array(input)
    normalized = normCoords(dataArray, x_min, x_max, y_min, y_max, z_min, z_max)
    
    n_r = (x_max - x_min)/size
    print()
    H, J = hashTable(normalized, n_r)
    
    voxelized = []
    for voxel in H.values():
        x, y, z = centroid(dataArray, voxel)
        voxelized.append([x, y, z])
    
    if not idx:
        fileName = f"{input}_Voxel_{size}.txt"
    else:
        splitted = re.split('_', input)
        fileName = f"{'_'.join(splitted[:-2])}_Voxel_{size}.txt"
        
    with open(fileName, 'w', encoding = 'utf-8') as f_out:
        for pt in voxelized:
            f_out.write(f"{pt[0]}\t{pt[1]}\t{pt[2]}\n")
    print(f"File. {fileName} created.")
    
def clusterization(filename, sizeC, number, prefix, l1 = True):
    
    if l1:
        os.system(f"IHFL {filename} +norm=l1 +fc={sizeC} +bin=0.90 +mju=0.95 +l=1 +knn=50 +ns=100000 -n -s -e")
    else:
        os.system(f"IHFL {filename} +norm=l2 +fc={sizeC} +bin=0.90 +mju=0.95 +l=1 +knn=50 +ns=100000 -n -s -e")

    files = glob(f"./Data/*_l1_l1_*facil_all.txt")
    for file in files:
        shutil.move(file, f"./Data/{prefix}{number}.txt_Cluster_l1_{sizeC}.txt")
        
    files = glob(f"./Data/*_l2_l1_*facil_all.txt")
    for file in files:
        shutil.move(file, f"./Data/{prefix}{number}.txt_Cluster_l2_{sizeC}.txt")
        
    # Get rid of *facil2.txt
    files = glob(f"./Data/*facil2.txt")
    for file in files:
        os.remove(file)
            
    # Get rid of *facil_stat.txt
    files = glob(f"./Data/*facil_stat.txt")
    for file in files:
        os.remove(file)
        
    # Get rid of *.dxf
    files = glob(f"./Data/*.dxf")
    for file in files:
        os.remove(file)
            
    # Get rid of *.txt_0_0_0
    files = glob(f"./Data/*.txt_[0-9]_[0-9]_[0-9]")
    for file in files:
        os.remove(file)
            
    # Get rid of *.txt.list
    files = glob(f"./Data/*.txt.list")
    for file in files:
        os.remove(file)

# fileName = f"Rauenstein_tree_all_"
fileName = f"tree_"
# fileName = f"via_ferrata_tree_"

sizeCluster = [0.07, 0.21, 0.28, 0.35]
sizeVoxel = [0.14, 0.42, 0.56, 0.7]
# for number in [6, 16, 18]:
for number in range(1, 27):   # Velká Pleš
# for number in range(1, 23):   # Rauenstein
# for number in [1]:            # Via ferrata
    fileNamesVoxel = [  f"./Data/{fileName}{number}.txt", 
                        f"./Data/{fileName}{number}.txt_Voxel_0.14.txt", 
                        f"./Data/{fileName}{number}.txt_Voxel_0.42.txt", 
                        f"./Data/{fileName}{number}.txt_Voxel_0.56.txt"]

    fileNamesCluster1 = [   f"./Data/{fileName}{number}.txt", 
                            f"./Data/{fileName}{number}.txt_Cluster_l1_0.07.txt", 
                            f"./Data/{fileName}{number}.txt_Cluster_l1_0.21.txt", 
                            f"./Data/{fileName}{number}.txt_Cluster_l1_0.28.txt"]
    
    fileNamesCluster2 = [   f"./Data/{fileName}{number}.txt", 
                            f"./Data/{fileName}{number}.txt_Cluster_l2_0.07.txt", 
                            f"./Data/{fileName}{number}.txt_Cluster_l2_0.21.txt", 
                            f"./Data/{fileName}{number}.txt_Cluster_l2_0.28.txt"]
    
    for idx, (sizeV, sizeC) in  enumerate(zip(sizeVoxel, sizeCluster)):
        voxelization(fileNamesVoxel[idx], sizeV, idx)
        
        clusterization(fileNamesCluster1[idx], sizeC, number, fileName, l1 = True)
        clusterization(fileNamesCluster2[idx], sizeC, number, fileName, l1 = False)
    
       