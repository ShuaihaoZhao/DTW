import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data=pd.read_csv(r'E:\U_of_A\ECE910\Solar Data (DTWA)\DTW\blatchford_202101.csv',
                      encoding = "ISO-8859-1", engine='python')
data['date']=pd.to_datetime(data['date'])
energy=pd.read_csv(r'E:\U_of_A\ECE910\Solar Data (DTWA)\DTW\energy_2021.csv',
                      encoding = "ISO-8859-1", engine='python')

energy_5=pd.read_csv(r'E:\U_of_A\ECE910\Solar Data (DTWA)\DTW\energy_5_sites.csv',
                      encoding = "ISO-8859-1", engine='python')[0:3102]

#sort the energy by date time and reset index
energy['date']=pd.to_datetime(energy['date'])
energy=energy.sort_values(by='date')
energy = energy.reset_index(drop=True)

energy_5['date']=pd.to_datetime(energy_5['date'])
energy_5=energy_5.sort_values(by='date')
energy_5=energy_5.reset_index(drop=True)



#a=data['irradiance'][0:24]
#a=energy['energy'][0:48]/26280
#b=energy_5['energy'][0:34]/6896


#test time seriesa
a = pd.Series([1,3,5,5,6,8,9,10,11,7,5,6,5,6,2,1])
b = pd.Series([0,0,0,0,0,0,0,0,2,4,6,6,6,7,9,10,10,11,12,8,6,5,4,5,1,0])
1
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
#    print(matrix)
    return matrix
    
    
def dtw_distance(cost_matrix):
    d=[]
    path=[]
    row_index=len(cost_matrix)-1
    col_index=len(cost_matrix[0])-1
    d.append(cost_matrix[row_index,col_index])
    path.append([row_index,col_index])
    while row_index!=0 or col_index!=0:
        if row_index>0 and col_index>0:
            if cost_matrix[row_index-1,col_index]<cost_matrix[row_index,col_index-1] and cost_matrix[row_index-1,col_index]<cost_matrix[row_index-1,col_index-1]:
                d.append(cost_matrix[row_index-1,col_index])
                row_index=row_index-1
                path.append([row_index,col_index])
            elif cost_matrix[row_index,col_index-1]<=cost_matrix[row_index-1,col_index] and cost_matrix[row_index,col_index-1]<cost_matrix[row_index-1,col_index-1]: 
                d.append(cost_matrix[row_index,col_index-1])
                col_index=col_index-1
                path.append([row_index,col_index])
            elif cost_matrix[row_index-1,col_index-1]<=cost_matrix[row_index-1,col_index] and cost_matrix[row_index-1,col_index-1]<=cost_matrix[row_index,col_index-1]: 
                d.append(cost_matrix[row_index-1,col_index-1])
                col_index=col_index-1
                row_index=row_index-1
                path.append([row_index,col_index])
        elif row_index==0 and col_index>0:
            d.append(cost_matrix[row_index,col_index-1])
            col_index=col_index-1
            path.append([row_index,col_index])
        elif row_index>0 and col_index==0:
            d.append(cost_matrix[row_index-1,col_index])
            row_index=row_index-1
            path.append([row_index,col_index])
            
    print('The DTW distance is: ',round(np.sum(d)/len(d),4))
#    print(path)
#    print(d)
    return path
    

c_matrix=dtw_cost(a,b)
path_pair=dtw_distance(c_matrix)

path_x = [p[1] for p in path_pair]
path_y = [p[0] for p in path_pair]

path_xx = [x+0.5 for x in path_x]
path_yy = [y+0.5 for y in path_y]

fig, ax = plt.subplots(figsize=(12, 12))
ax = sns.heatmap(c_matrix, cmap="YlGnBu",square=True, linewidths=0.1,ax=ax)
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top - 0.5)
ax.invert_yaxis()

ax.plot(path_xx, path_yy, color='red', linewidth=3, alpha=0.5)

plt.figure(figsize=(12,12))
plt.plot(a.index,a,color='b',label='date set 1')
plt.plot(b.index,b,color='r',label='date set 1')
plt.title('Energy Data Plot')
plt.xlabel('Index')
plt.ylabel('Normalized')
plt.legend(loc="upper left")

for i in range(len(path_pair)):
    x1=path_pair[i][0]
    x2=path_pair[i][1]
    y1=a[x1]
    y2=b[x2]
    temp=[[x1,x2],[y1,y2]]
    plt.scatter(temp[0],temp[1],marker='o',color='k');
    plt.plot(temp[0],temp[1],'--',color='k',alpha=0.3)
    
plt.show()  
    
