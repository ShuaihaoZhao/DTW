import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_csv(r'E:\U_of_A\ECE910\Solar Data (DTWA)\DTW\blatchford_202101.csv',
                      encoding = "ISO-8859-1", engine='python')
energy=pd.read_csv(r'E:\U_of_A\ECE910\Solar Data (DTWA)\DTW\energy_2021.csv',
                      encoding = "ISO-8859-1", engine='python')

a=data['temperature'][0:5]
b=data['windSpeed'][0:4]

series1 = pd.Series([1,4,5,10,9,3,2,6,8,4])
series2 = pd.Series([1,7,3,4,1,10,5,4,7,4])

def dtw_cost(ts1,ts2):
    len_1=len(ts1)
    len_2=len(ts2)
    matrix=np.zeros((len_1,len_2))#length ts1 rows, length ts2 columes
    for i in range(len_1):
        for j in range(len_2):
            matrix[i,j]=np.inf
    matrix[0,0]=0
    for i2 in range(len_1):
        for j2 in range(len_2):
            if(i2 != 0 and j2 != 0):
                matrix[i2,j2]=abs(ts1[i2]-ts2[j2])+np.min([matrix[i2-1,j2],matrix[i2,j2-1],matrix[i2-1,j2-1]])
            elif i2 == 0 and j2 != 0:
                matrix[i2,j2]=abs(ts1[i2]-ts2[j2])+matrix[i2,j2-1]
            elif i2 != 0 and j2 == 0:
                matrix[i2,j2]=abs(ts1[i2]-ts2[j2])+matrix[i2-1,j2]
#    return matrix
    print(matrix)
    
    
#cost=dtw_cost(a,b)
dtw_cost(series1,series2)