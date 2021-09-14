import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

def ConvertCoord(data, df):
    """
    Cria novo dataframe com as coordenadas de pixels da imagem a fim de 
    conseguirmos plotar os pontos de interesse em cima do mapa.

    Args:
        data (np.darray): Matriz da imagem.
        df (pd.DataFrame): DataFrame original.

    Returns:
        pd.DataFrame: [description]
    """
    
    n, m, _ = data.shape
    
    df_new = df.copy()
    
    for i, column in enumerate(['x', 'y']):
        df_new[column] = df_new[column] / df_new[column].iloc[-1]
        
    df_new['y'] = n * df_new['y']
    df_new['x'] = m * df_new['x']
    
    return df_new 

# fazendo caminho
full_path = os.getcwd()
cenario_name = '/Cenarios/Cenario1/' # selecione a pasta de qual cenário voce deseja (Ex: Cenario1)
path_cenario = full_path + cenario_name


# leio DataFrame com os pontos.
df_pts = pd.read_csv( path_cenario + 'Coord-Localidades.csv', header= None)
df_pts = df_pts.rename(columns = {0:'x', 1:'y'})

# leio DataFrame das labels.
df_labels = pd.read_csv( path_cenario + 'Labels-Localidades.csv', sep = ';', header= None)
df_labels = df_labels.rename(columns = {0:'labels'})

dataFrames = [df_labels, df_pts]
df = pd.concat(dataFrames, axis=1) # Merge

# pego os dados da imagem usada na determinação dos pontos.
data = plt.imread( path_cenario + 'Imagem-Aerea.jpg')

# crio novo dataframe com as coordenadas no sistema de coordenadas
# dos pixels da imagem 
df_new = ConvertCoord(data, df)


# plot
n = 3.5 #ajuste o tamanho da imagem
plt.rcParams["figure.figsize"] = [n*7.00, n*3.50]
plt.rcParams["figure.autolayout"] = False

im = plt.imshow(data)

m, n, _ = data.shape
plt.xlim(0, n)
plt.ylim(m, 0)

plt.scatter(df_new['x'], df_new['y'], color = 'yellow')
for i, label in enumerate(df_new['labels']):
    plt.text(df_new['x'][i], df_new['y'][i]-25, label, color = 'white', size = 15)

plt.savefig( path_cenario + 'MapaPontos.pdf')


# salve o arquivo .csv com as coordenadas em m 
df.to_csv( path_cenario + 'Coordinates.csv')

