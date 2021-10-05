# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dJo5Sq58kXfvvqjas38LE2krCb75_VM5
"""

!pip install matplotlib==3.1.3
!pip install osmnet
!pip install folium

!pip install rtree
!pip install pygeos
!pip install geojson
!pip install geopandas

from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import osmnet
import folium
import rtree
import pygeos
import geojson
import geopandas as gpd

!git clone https://github.com/CityScope/CSL_HCMC

file = gpd.read_file("/content/CSL_HCMC/Data/GIS/Population/population_HCMC/population_shapefile/Population_District_Level.shp")

!git clone https://github.com/ThienPhuoc19522057/json

click = gpd.read_file("/content/json/14-09.json")

file["Tocdo"] = file["Pop_2019"]/file["Pop_2017"]
lst = list(file.sort_values("Tocdo", ascending=False)["Dist_Name"].head(10))
print("Top 10 quận/huyện có tốc độ tăng dân số lớn nhất là: ")
for i in lst:
  print("+ " + str(i))

from geopandas.tools import sjoin

click= click.to_crs(epsg=4326)
click.crs
file=file.to_crs(epsg=4326)

filter_click = gpd.sjoin(click,file, how="left", op="within")
filter_click.head()

filter_click_lst = filter_click[filter_click.Dist_Name.isin(lst)]
filter_click_lst

District9=filter_click_lst[filter_click_lst["Dist_Name"]=="District 9"]
HocMon=filter_click_lst[filter_click_lst['Dist_Name']=="Hoc Mon"]
NhaBe=filter_click_lst[filter_click_lst['Dist_Name']=="Nha Be"]
District12=filter_click_lst[filter_click_lst['Dist_Name']=="District 12"]
District2=filter_click_lst[filter_click_lst['Dist_Name']=="District 2"]
CuChi=filter_click_lst[filter_click_lst['Dist_Name']=="Cu Chi"]
District7=filter_click_lst[filter_click_lst['Dist_Name']=="District 7"]
ThuDuc=filter_click_lst[filter_click_lst['Dist_Name']=="Thu Duc"]
BinhChanh=filter_click_lst[filter_click_lst['Dist_Name']=="Binh Chanh"]
BinhTan=filter_click_lst[filter_click_lst['Dist_Name']=="Binh Tan"]

"""#Quận 9"""

def createdata(heatmapdata,a):
  lst_point=[]
  for i in a['geometry']:
    lst_point.append([i.y,i.x])
  print(len(lst_point))
  kmeans = KMeans(n_clusters=20, random_state=1).fit(lst_point)
  labels = kmeans.labels_
  print(len(labels))
  unique, counts = np.unique(labels, return_counts=True)
  dic=dict(zip(unique, counts))
  max_label = max(dic, key=dic.get)
  print(max_label)
  index_maxlabel = []
  for i in range(len(labels)):
    if labels[i]==max_label:
      index_maxlabel.append(i) 
  print(len(index_maxlabel))
  for i in index_maxlabel:
    heatmapdata.append(lst_point[i])
  print(len(heatmapdata))
data=[]
createdata(data,District9)

createdata(data,District12)

createdata(data,District2)

createdata(data,District7)

createdata(data,NhaBe)

createdata(data,BinhChanh)

createdata(data,BinhTan)

createdata(data,CuChi)

createdata(data,ThuDuc)

createdata(data,HocMon)

"""#Vẽ Heatmap"""

data

import folium
m = folium.Map(location=[10.8, 107], zoom_start=10, tiles='CartoDB positron')

from folium.plugins import HeatMap
HeatMap(data).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))
m

m.save("heatmap.png")