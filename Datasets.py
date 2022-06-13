#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/azunig/kul-mda-a1/blob/1st_steps/Description_of_Datasets.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Cities and Greenhouse Gas Emissions datasets

# Initial dataset from [data.cdp.net](https://data.cdp.net)

# In[ ]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# 
# 
# Proposed Research Question:  
# - Are all cities reporting consistent data ? 
# - Are there data gaps in some regions ? 
# - Are the emission improving ?
# - Is there a link with the population density ?

# In[ ]:


#api json to dataframe 2019-2020
df20 = pd.read_json("https://data.cdp.net/resource/p43t-fbkj.json")
df19 = pd.read_json("https://data.cdp.net/resource/542d-zyj8.json")


# In[ ]:


#https://data.cdp.net/Governance/2020-Full-Cities-Dataset/eja6-zden
quest = pd.read_json("https://data.cdp.net/resource/eja6-zden.json") #questionnaire


# In[ ]:


#rename columns 2019
df19 = df19.rename(columns={"inventory_boundary": "administrative_city_boundary", 
                            "common_reporting_framework_inventory_format_gpc": "common_reporting_framework",
                            "direct_emissions_scope_1_metric_tonnes_co2e_for_total_generation_of_grid_supplied_energy": "direct_emissions_metric_tonnes",
                           "direct_emissions_scope_1_metric_tonnes_co2e_for_total_emissions_excluding_generation_of_grid_supplied_energy": "direct_emissions_metric_tonnes_1",
                           "indirect_emissions_from_use_of_grid_supplied_energy_scope_2_metric_tonnes_co2e_for_total_generation_of_grid_supplied_energy": "indirect_emissions_from_use",
                           "indirect_emissions_from_use_of_grid_supplied_energy_scope_2_metric_tonnes_co2e_for_total_emissions_excluding_generation_of_grid_supplied_energy": "indirect_emissions_from_use_1",
                           "emissions_occurring_outside_city_boundary_scope_3_metric_tonnes_co2e_for_total_generation_of_grid_supplied_energy": "emissions_occurring_outside",
                           "emissions_occurring_outside_city_boundary_scope_3_metric_tonnes_co2e_for_total_emissions_excluding_generation_of_grid_supplied_energy": "emissions_occurring_outside_1",
                           "total_scope_1_emissions_metric_tonnes_co2e": "total_scope_1_emissions_metric",
                           "total_scope_2_emissions_metric_tonnes_co2e": "total_scope_2_emissions_metric",
                           "reason_for_change": "primary_reason_for_the_change"})


# In[ ]:


df = pd.concat([df19, df20])


# In[ ]:


print(df.head())


# In[ ]:


print(quest.head())


# In[ ]:


size = df.size 
  
# dataframe.shape 
shape = df.shape 
  
# dataframe.ndim 
df_ndim = df.ndim 
  
# series.ndim 
series_ndim = df["total_scope_1_emissions_metric"].ndim 
  
# printing size and shape 
print("Size = {}\nShape ={}\nShape[0] x Shape[1] = {}". 
format(size, shape, shape[0]*shape[1])) 
  
# printing ndim 
print("ndim of dataframe = {}\nndim of series ={}". 
format(df_ndim, series_ndim)) 


# In[ ]:


#for col in df.columns: 
#    print(col)
    
df.info()


# In[ ]:


df.isna().sum()


# In[ ]:


df['direct_emissions_metric_tonnes'].describe()


# In[ ]:


pd.crosstab(index = df['year_reported_to_cdp'], columns = 'count')


# In[ ]:


gpby=df.groupby(["year_reported_to_cdp","cdp_region"]).size()
print(gpby)


# In[ ]:


df.groupby(["country", "year_reported_to_cdp"]).size().reset_index(name="Reports")


# In[ ]:


#df = df[df['direct_emissions_metric_tonnes'].notna()]
print('Dimensions of the dataset:',df.shape)
print('Dimensions after removing columns:',df.dropna(axis=1).shape)
#df = df.dropna(subset = ['direct_emissions_metric_tonnes', 'indirect_emissions_from_use'])


# In[ ]:


print(df)


# In[ ]:


plt.plot(np.array(df['direct_emissions_metric_tonnes']))
plt.show()


# In[ ]:


fig1 = plt.plot(np.array(df['direct_emissions_metric_tonnes']), c = "red", label = "direct emissions")
plt.plot(np.array(df['indirect_emissions_from_use']), c = "blue", label = "indirect emissions")
plt.title("Emissions")
plt.legend()
plt.grid()


plt.show()


# In[ ]:


plt.scatter(np.array(df["direct_emissions_metric_tonnes"]),np.array(df[":@computed_region_n7dz_xzkg"]), 
            c = np.array(df["indirect_emissions_from_use"]), s = 100, marker='+')
plt.xlabel("direct_emissions")
plt.ylabel("regions")
plt.title("This is the second plot")
#plt.xlim([20,70])
#plt.xticks(np.linspace(25,65,8), rotation = 90)
plt.colorbar(label = "Indirect emissions")
plt.grid()
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




