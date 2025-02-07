# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 22:02:25 2024

@author: cheik
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors  
import matplotlib.cm as cm  


file_path = r'C:/Users/cheik/Downloads/Terres arables.xlsx'
df = pd.read_excel(file_path, sheet_name='Data')


print("Vérification du fichier Excel :")
print(df.head())


df_cleaned = df.dropna(how='all')  
df_cleaned = df_cleaned.dropna(axis=1, how='all')  
df_cleaned.columns = df_cleaned.columns.str.strip()


df_cleaned.columns = df_cleaned.iloc[0]  
df_cleaned = df_cleaned.drop(2) 

df_cleaned = df_cleaned.reset_index(drop=True)
df_cleaned.columns.name = None  

print("Colonnes du dataframe nettoyé :")
print(df_cleaned.columns)


print("Premières lignes du dataframe nettoyé :")
print(df_cleaned.head())


df_cleaned.iloc[:, 2:] = df_cleaned.iloc[:, 2:].apply(pd.to_numeric, errors='coerce')


df_cleaned['Average_Terres_Arables'] = df_cleaned.iloc[:, 2:].mean(axis=1)


shapefile_path = r'C:/Users/cheik/OneDrive/Bureau/maps/ne_110m_admin_0_countries.shp'
world = gpd.read_file(shapefile_path)


print("Colonnes du shapefile :")
print(world.columns)


print("Premières lignes du shapefile :")
print(world.head())


df_cleaned['Country Name'] = df_cleaned['Country Name'].replace({
    'United States': 'United States of America',
    'Russia': 'Russian Federation',
    
})


merged_data = world.merge(df_cleaned[['Country Name', 'Average_Terres_Arables']], left_on='NAME', right_on='Country Name', how='left')


print("Fusion des données :")
print(merged_data.head())


merged_data['Average_Terres_Arables'] = merged_data['Average_Terres_Arables'].fillna(0)


fig, ax = plt.subplots(1, 1, figsize=(15, 10))


cmap = 'YlOrRd'
norm = mcolors.Normalize(vmin=merged_data['Average_Terres_Arables'].min(), vmax=merged_data['Average_Terres_Arables'].max())

merged_data.plot(column='Average_Terres_Arables', ax=ax, legend=False, cmap=cmap)

sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])


cbar = fig.colorbar(sm, ax=ax, orientation='horizontal', pad=0.05)
cbar.set_label("Terres arables moyennes (hectares)\nAuteur : SheikhAlSamad")


plt.title('Terres arables moyennes par pays (1960-2020)', fontsize=15)
plt.show()
