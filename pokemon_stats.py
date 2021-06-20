
import csv
import numpy as np
import math
import random
import matplotlib.pyplot as plt

def load_data(filepath):
     count = 0
     Pokemon_Dictionary = [];
     with open(filepath,encoding='UTF-8') as csvfile:
         reader = csv.DictReader(csvfile)
         for row in reader:
             dic = {};
             dic['#'] = row['#']
             dic['Total'] = row['Total']
             dic['HP'] = row['HP']
             dic['Attack'] = row['Attack']
             dic['Defense'] = row['Defense']
             dic['Sp. Atk'] = row['Sp. Atk']
             dic['Sp. Def'] = row['Sp. Def']
             dic['Speed'] = row['Speed']
             Pokemon_Dictionary.append(dic)
             count = count + 1
             if(count >= 20):
                break  
     return Pokemon_Dictionary
 
def calculate_x_y(stats):
    x = int(stats['Attack']) + int(stats['Sp. Atk']) + int(stats['Speed'])
    y = int(stats['HP']) + int(stats['Defense']) + int(stats['Sp. Def'])
    return (x,y)

def hac(dataset):
    distance = []
    cluster = {}
    output = []
    for i in range(0,len(dataset)):
        if(math.isnan(dataset[i][0]) == True or math.isnan(dataset[i][1]) == True 
           or math.isinf(dataset[i][0]) == True or math.isinf(dataset[i][1]) == True):
           del dataset[i]
    m = len(dataset)
    
    for i in range(0,m):
        cluster[i] = i
        
    for i in range(0,m):
        row = []
        for j in range(0,m):
            row.append(math.dist(dataset[i],dataset[j]))
        distance.append(row)
    
    max = np.max(distance)
    for i in range(0,m):
        distance[i][i] = max + 1
    
    t = True
    count = 0
    while t :
        row1 = []
        minDis = np.min(distance)
        f= np.argwhere(distance == np.min(distance))
        min1 = np.min(f)
        max1 = np.max(f)
        if(len(f) <= 2):
           f[0].sort()
           min2 = f[0][1]
        if(len(f) > 2):
           g = []
           for i in range(0,len(f)):
               if min1 in f[i]:
                   f[i].sort()
                   f[i][0] = max1
                   g.append(f[i])
           min2 = np.min(g)
        distance[min1][min2] = max
        distance[min2][min1] = max       
        if(cluster[min1] != cluster[min2]):
            if(cluster[min1] < cluster[min2]):
               min3 = cluster[min1]
               min4 = cluster[min2]
            elif(cluster[min1] > cluster[min2]):
               min3 = cluster[min2]    
               min4 = cluster[min1]  
            row1.append(min3)
            row1.append(min4)
            row1.append(minDis)
            newCluster = m + count
            count = count + 1
            count1 = 0
            for i in range(0,m):
                if (cluster[i] == min3 or cluster[i] == min4):
                    cluster[i] = newCluster
                    count1= count1 + 1
            row1.append(count1)
            output.append(row1)
        count2 = 0
        for i in range(0,m):
            if(cluster[i] != newCluster):
                count2 = count2 + 1
        if(count2 == 0):
            t = False
        data = np.array(output)
    return data

def hacshow(dataset):
    distance = []
    cluster = {}
    for i in range(0,len(dataset)):
        if(math.isnan(dataset[i][0]) == True or math.isnan(dataset[i][1]) == True 
           or math.isinf(dataset[i][0]) == True or math.isinf(dataset[i][1]) == True):
           del dataset[i]
    m = len(dataset)
    
    for i in range(0,m):
        cluster[i] = i
        
    for i in range(0,m):
        row = []
        for j in range(0,m):
            row.append(math.dist(dataset[i],dataset[j]))
        distance.append(row)
    
    max = np.max(distance)
    for i in range(0,m):
        distance[i][i] = max + 1
    
    t = True
    count = 0
    while t :
        f= np.argwhere(distance == np.min(distance))
        min1 = np.min(f)
        max1 = np.max(f)
        if(len(f) <= 2):
           f[0].sort()
           min2 = f[0][1]
        if(len(f) > 2):
           g = []
           for i in range(0,len(f)):
               if min1 in f[i]:
                   f[i].sort()
                   f[i][0] = max1
                   g.append(f[i])
           min2 = np.min(g)
        distance[min1][min2] = max
        distance[min2][min1] = max       
        if(cluster[min1] != cluster[min2]):
            x = []
            y = []
            x.append(dataset[min1][0])
            x.append(dataset[min2][0])
            y.append(dataset[min1][1])
            y.append(dataset[min2][1])
            plt.plot(x,y)
            if(cluster[min1] < cluster[min2]):
               min3 = cluster[min1]
               min4 = cluster[min2]
            elif(cluster[min1] > cluster[min2]):
               min3 = cluster[min2]    
               min4 = cluster[min1]  
            newCluster = m + count
            count = count + 1
            for i in range(0,m):
                if (cluster[i] == min3 or cluster[i] == min4):
                    cluster[i] = newCluster
        count2 = 0
        for i in range(0,m):
            if(cluster[i] != newCluster):
                count2 = count2 + 1
        plt.pause(0.1)
        if(count2 == 0):
            t = False
            plt.pause(5)
    
def random_x_y(m):
    hac_input = []
    for i in range(0,m):
        x = random.randint(1,359)
        y = random.randint(1,359)
        hac_input.append((x,y))
    return hac_input

def imshow_hac(dataset):
    x = []
    y = []
    for i in range(0,len(dataset)):
        x.append(dataset[i][0])
        y.append(dataset[i][1])
    plt.scatter(x,y)
    hacshow(dataset)
    plt.show()

   

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
