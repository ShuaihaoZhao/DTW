
import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_csv(r'E:\U_of_A\ECE910\Solar Data (DTWA)\DTW\blatchford_202101.csv',
                      encoding = "ISO-8859-1", engine='python')
energy=pd.read_csv(r'E:\U_of_A\ECE910\Solar Data (DTWA)\DTW\energy_2021.csv',
                      encoding = "ISO-8859-1", engine='python')
data.head()