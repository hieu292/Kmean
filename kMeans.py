#----------------------------------------------------------------------
# kMeans.py
#
#
# Author: Nguyen Huy Hieu - nguyen.huy.hieu292@gmail.com
#
#----------------------------------------------------------------------
from numpy import *
import numpy as np
import matplotlib, matplotlib.pyplot as plt
from matplotlib.mlab import PCA
from mpl_toolkits.mplot3d import Axes3D
import csv

class kmean:
    def __init__(self):   
        self.calculate =0   # number recalculate centroid
        self.error = []
    #   self.num_cluster
    #   self.row
    #   self.col
    #   self.tem_array          store error array
    #   self.store_centroid     store centroid array
    #   self.final_Centroids
    #   self.temporary_Centroids
    #   self.final_clusterAssment
    #   self.temporary_clusterAssment
    def set_num_cluster(self,k):
        self.num_cluster = k
    def loadDataSet(self,fileName):      #general function to parse tab -delimited floats
        dataMat = []                #assume last column is target value
        fr = open(fileName)
        for line in fr.readlines():
            curLine = line.strip().split('\t')
            fltLine = map(float,curLine) #map all elements to float()
            dataMat.append(fltLine)
        return dataMat
    def randCent(self,dataSet):
        n = shape(dataSet)[1]
        self.col = n
        self.store_centroid = asmatrix(zeros((1,n)))
        centroids = asmatrix(zeros((self.num_cluster,n)))#create centroid mat - asmatrix() is function to convert n-array to matrix
        for j in range(n):#create random cluster centers, within bounds of each dimension
            minJ = min(dataSet[:,j]) 
            rangeJ = float(max(dataSet[:,j]) - minJ)
            centroids[:,j] = asmatrix(minJ + rangeJ * random.rand(self.num_cluster,1))
        return centroids
    def distEclud(self,vecA, vecB):
        return sqrt(sum(power(vecA - vecB, 2))) #la.norm(vecA-vecB)
    def kMeans_compute(self,dataSet):
        m = shape(dataSet)[0]
        self.row = m
        clusterAssment = asmatrix(zeros((m,2)))#create mat to assign data points 
        self.tem_array = np.zeros((1,2))                             #to a centroid, also holds SE of each point
        centroids = self.randCent(dataSet)
	
        count_var = 1
        clusterChanged = True
	
        while clusterChanged:
            clusterChanged = False
            for i in range(m):#for each data point assign it to the closest centroid
                minDist = inf; minIndex = -1
                for j in range(self.num_cluster):
                    distJI = self.distEclud(centroids[j,:],dataSet[i,:])
                    if distJI < minDist:
                        minDist = distJI; minIndex = j
                if clusterAssment[i,0] != minIndex:
                    clusterChanged = True
                clusterAssment[i,:] = minIndex,minDist**2
            # print "Centroid thu %d:" %(count_var)
            # print centroids
            self.store_centroid = np.concatenate((self.store_centroid,centroids))
            self.calculate = count_var
            self.tem_array = np.concatenate((self.tem_array,clusterAssment))
            for cent in range(self.num_cluster):   #recalculate centroids
                ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]#get all the point in this cluster
                centroids[cent,:] = mean(ptsInClust, axis=0) #assign centroid to mean - mean() is function to calculate average
            count_var+=1
        return centroids,clusterAssment

    def pca_compute(self,datMat,myCentroids):
        centroid_array = asarray(myCentroids)
        new_datMat = concatenate((asarray(datMat),centroid_array))
        dataMat_pca = PCA(new_datMat)
        dataMat_pca.fracs
        return dataMat_pca
    def extract_2_dimetion(self,dataMat_pca,jarray):   # input of jarray = clusterAssment (from kMeans_compute())  or  b (from split_each_centroid)
        a = np.zeros((self.num_cluster+1,100))
        b = np.zeros((self.num_cluster+1,100))
        for p in range(self.num_cluster):
            count1 = 0
            for t in range(self.row):
                if jarray[t,0] == p:
                    a[p,count1]=dataMat_pca.Y[t,0]
                    b[p,count1]=dataMat_pca.Y[t,1]
                    count1 = count1 + 1
        count2 = 0
        for u in range(self.row,self.row + self.num_cluster):
            a[self.num_cluster,count2]=dataMat_pca.Y[u,0]
            b[self.num_cluster,count2]=dataMat_pca.Y[u,1]
            count2 = count2 + 1
        return a,b
    def extract_3_dimetion(self,dataMat_pca,jarray): # input of jarray = clusterAssment (from kMeans_compute())  or  b (from split_each_centroid)
        a = np.zeros((self.num_cluster+1,100))
        b = np.zeros((self.num_cluster+1,100))
        c = np.zeros((self.num_cluster+1,100))
        for p in range(self.num_cluster):
            count1 = 0
            for t in range(self.row):
                if jarray[t,0] == p:
                    a[p,count1]=dataMat_pca.Y[t,0]
                    b[p,count1]=dataMat_pca.Y[t,1]
                    c[p,count1]=dataMat_pca.Y[t,2]
                    count1 = count1 + 1
        count2 = 0
        for u in range(self.row,self.row + self.num_cluster):
            a[self.num_cluster,count2]=dataMat_pca.Y[u,0]
            b[self.num_cluster,count2]=dataMat_pca.Y[u,1]
            c[self.num_cluster,count2]=dataMat_pca.Y[u,1]
            count2 = count2 + 1
        return a,b,c
    def plot2D(self,mang1,mang2):
        fig = plt.figure() # create figure and axes
        ax = fig.add_subplot(111) # split the page into a 1x1 array of subplots and put me in the first one (111) (as a matter of fact, the only one)
        color = ['blue','green','yellow','Gray','brown','orange','purple','pink','red','white','black']
        for t in range(self.num_cluster + 1):
            a = mang1[t,:]
            b = mang2[t,:]
            ax.scatter(a[np.nonzero((a))],b[np.nonzero((b))], color=color[t], marker='o', s=100)
        plt.show()
    def plot3D(self,mang1,mang2,mang3):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        color = ['blue','green','yellow','Gray','brown','orange','purple','pink','red','white','black']
        for t in range(self.num_cluster + 1):
            a = mang1[t,:]
            b = mang2[t,:]
            c = mang3[t,:]
            ax.scatter(a[np.nonzero((a))],b[np.nonzero((b))],c[np.nonzero((c))], color=color[t], marker='o')
        plt.show()
    def plotError(self):
        n=self.row
        b = []
        
        for i in range(self.calculate):
            a = 0
            for k in range(1,n+1):
                a = a + self.tem_array[k+i*n,1]
            b.append(a)
            
        q = []
        for p in range(1,self.calculate+1):
            q.append(p)
        plt.plot(q,b,color='red',marker='o')
        plt.show()
    def split_each_centroid(self,k):
        n=self.row
        f1 = 1+(k-1)*n
        f2 = n+1+(k-1)*n
        a = self.tem_array[f1:f2,:]
        n1 = (k-1)*3+1
        n2 = (k-1)*3+self.num_cluster+1
        b = self.store_centroid[n1:n2,:]
        return b,a           # a is classfy each point when use centroid is b
		# the result return is same kMeans_compute()
    def save_file(self):
        with open('dataset.csv','r') as csvinput:
            with open('output.csv', 'w') as csvoutput:
                writer = csv.writer(csvoutput, lineterminator='\n')
                reader = csv.reader(csvinput)

                all = []
                row = next(reader)
                row.append('Classyfication')
                all.append(row)
                i=0
                for row in reader:
                    row.append(self.final_clusterAssment[i,0])
                    all.append(row)
                    i=i+1

                writer.writerows(all)
        

        
    def run1(self):
        self.datMat=mat(self.loadDataSet("dataset.txt"))
        self.final_Centroids,self.final_clusterAssment = self.kMeans_compute(self.datMat)
        b = self.pca_compute(self.datMat,self.final_Centroids)
        self.t1,self.t2 = self.extract_2_dimetion(b,self.final_clusterAssment)
        self.t3,self.t4,self.t5 = self.extract_3_dimetion(b,self.final_clusterAssment)
    def run2(self,k):
        self.temporary_Centroids,self.temporary_clusterAssment = self.split_each_centroid(k)
        a = self.pca_compute(self.datMat,self.temporary_Centroids)
        self.u1,self.u2 = self.extract_2_dimetion(a,self.temporary_clusterAssment)
        self.u3,self.u4,self.u5 = self.extract_3_dimetion(a,self.temporary_clusterAssment)
    def run3(self):
        self.plot2D(self.u1,self.u2)
    def run4(self):
        self.plot3D(self.u3,self.u4,self.u5)
    def run5(self):
        self.plot2D(self.t1,self.t2)
    def run6(self):
        self.plot3D(self.t3,self.t4,self.t5)
    def run7(self):
        self.plotError()
        
