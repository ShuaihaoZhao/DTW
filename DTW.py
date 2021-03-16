import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_csv(r'E:\U_of_A\ECE910\Solar Data (DTWA)\DTW\blatchford_202101.csv',
                      encoding = "ISO-8859-1", engine='python')
energy=pd.read_csv(r'E:\U_of_A\ECE910\Solar Data (DTWA)\DTW\energy_2021.csv',
                      encoding = "ISO-8859-1", engine='python')

a=data['temperature'][0:24]
b=data['windSpeed'][0:24]
#
#series1 = pd.Series([1,1,4,10,9,3,2,6,8,4])
#series2 = pd.Series([1,4,10,9,3,2,6,8,4,4])

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
    return matrix
#    print(matrix)
    
    
def dtw_distance(cost_matrix):
    d=[]
    row_index=len(cost_matrix)-1
    col_index=len(cost_matrix[0])-1
    d.append(cost_matrix[row_index,col_index])
    while row_index!=0 and col_index!=0:
        if row_index>0 and col_index>0:
            if cost_matrix[row_index-1,col_index]<cost_matrix[row_index,col_index-1] and cost_matrix[row_index-1,col_index]<cost_matrix[row_index-1,col_index-1]:
                d.append(cost_matrix[row_index-1,col_index])
                row_index=row_index-1
            elif cost_matrix[row_index,col_index-1]<cost_matrix[row_index-1,col_index] and cost_matrix[row_index,col_index-1]<cost_matrix[row_index-1,col_index-1]: 
                d.append(cost_matrix[row_index,col_index-1])
                col_index=col_index-1
            elif cost_matrix[row_index-1,col_index-1]<=cost_matrix[row_index-1,col_index] and cost_matrix[row_index-1,col_index-1]<cost_matrix[row_index,col_index-1]: 
                d.append(cost_matrix[row_index-1,col_index-1])
                col_index=col_index-1
                row_index=row_index-1
        elif row_index==0 and col_index>0:
            d.append(cost_matrix[row_index,col_index-1])
            col_index=col_index-1
        elif row_index>0 and col_index==0:
            d.append(cost_matrix[row_index-1,col_index])
            row_index=row_index-1
            
    print(round(np.sum(d)/len(d),4))
    
    
c_matrix=dtw_cost(a,b)
dtw_distance(c_matrix)