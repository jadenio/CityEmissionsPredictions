#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Cleaning-the-2012-2020-CDP-Datasets" data-toc-modified-id="Cleaning-the-2012-2020-CDP-Datasets-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Cleaning the 2012-2020 CDP Datasets</a></span><ul class="toc-item"><li><span><a href="#CDP-2012-Dataset" data-toc-modified-id="CDP-2012-Dataset-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>CDP 2012 Dataset</a></span></li><li><span><a href="#CDP-2013-Dataset" data-toc-modified-id="CDP-2013-Dataset-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>CDP 2013 Dataset</a></span></li><li><span><a href="#CDP-2014-Dataset" data-toc-modified-id="CDP-2014-Dataset-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>CDP 2014 Dataset</a></span></li><li><span><a href="#CDP-2015-Dataset" data-toc-modified-id="CDP-2015-Dataset-1.4"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>CDP 2015 Dataset</a></span></li><li><span><a href="#CDP-2016-Dataset" data-toc-modified-id="CDP-2016-Dataset-1.5"><span class="toc-item-num">1.5&nbsp;&nbsp;</span>CDP 2016 Dataset</a></span></li><li><span><a href="#CDP-2017-Dataset" data-toc-modified-id="CDP-2017-Dataset-1.6"><span class="toc-item-num">1.6&nbsp;&nbsp;</span>CDP 2017 Dataset</a></span></li><li><span><a href="#CDP-2018-2019-Dataset" data-toc-modified-id="CDP-2018-2019-Dataset-1.7"><span class="toc-item-num">1.7&nbsp;&nbsp;</span>CDP 2018-2019 Dataset</a></span></li><li><span><a href="#CDP-2019-Dataset" data-toc-modified-id="CDP-2019-Dataset-1.8"><span class="toc-item-num">1.8&nbsp;&nbsp;</span>CDP 2019 Dataset</a></span></li><li><span><a href="#CDP-2020-Dataset" data-toc-modified-id="CDP-2020-Dataset-1.9"><span class="toc-item-num">1.9&nbsp;&nbsp;</span>CDP 2020 Dataset</a></span></li></ul></li><li><span><a href="#Merging-years-datasets" data-toc-modified-id="Merging-years-datasets-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Merging years datasets</a></span></li><li><span><a href="#Save-data-to-csv" data-toc-modified-id="Save-data-to-csv-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Save data to csv</a></span></li></ul></div>

# # CDP emissions by city

# In[1]:


#Import required packages
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pycountry
import functools
import re


# In[2]:


# method to identify country code based on country name
@functools.lru_cache(None)
def do_fuzzy_search(country):
    try:   
        result = pycountry.countries.search_fuzzy(country)
    except Exception:
        return np.nan
    else:
        return result[0].alpha_3


# In[3]:


# fix indexes
Ind2 = ['Country Name', 'Country Code', 'City', 'Year'] 


# ## Cleaning the 2012-2020 CDP Datasets

# ### CDP 2012 Dataset

# In[4]:


#Import CDP 2012 Dataset
df2012 = pd.read_csv("https://raw.githubusercontent.com/jadenio/CityEmissionsData/main/CDP%202012-2020/2012_-_Citywide_GHG_Emissions.csv")
df2012.shape


# In[5]:


#Standardize country names 
df2012.loc[df2012['Country'] == 'USA', 'Country'] = 'United States'


# In[6]:


#Rename column names
df2012 = df2012.rename(columns={'Account No': "id",
                                'Country':'Country',
                                'City Short Name': 'City',
                                'City Name' : 'Municipality',
                                'Reporting Year' : 'Year_report',
                                'Measurement Year': 'Date_measure',
                               #'Current Population': 'Population',
                               #'Gases included': 'Gases' ,
                               'Total City-wide Emissions (metric tonnes CO2e)': 'TotalEmissions',                                
                               #'Total Scope 1 Emissions (metric tonnes CO2e)': 'EmissionsScope1',
                               #'Total Scope 2 Emissions (metric tonnes CO2e)': 'EmissionsScope2',
                               #'Land area (in square km)': 'Land_Area',
                               #'Average altitude (m)': 'Altitude',
                               #"Average annual temperature (in Celsius)": 'Temperature',
                               #'City GDP' : 'GDP',
                               #'Increase/Decrease from last year': 'Reduction'
                               })


# In[7]:


#Extract coordinates from "City Location" column into "Longitude" and "Latitude" columns 
df2012['Coords'] = df2012['City Location'].str.extract(r"\((.*?)\)", expand=False)
coord12 = df2012["Coords"].str.split(", ", n = 1, expand = True)
df2012["Longitude"]= coord12[1]
df2012["Latitude"]= coord12[0]

df2012.drop(['Coords', 'C40', 'City Location', 'Country Location', 'Primary Methodology', 'Methodology Details'], inplace=True, axis=1)


# In[8]:


df2012.columns


# In[9]:


#Drop all duplicate emissions data (some of the datasets slightly overlap)
df2012 = df2012.drop_duplicates(keep="first")#subset='TotalEmissions', 
df2012.shape


# ### CDP 2013 Dataset

# In[10]:


#Import CDP 2013 Dataset
df2013 = pd.read_csv("https://raw.githubusercontent.com/jadenio/CityEmissionsData/main/CDP%202012-2020/Citywide_GHG_Emissions_2013.csv")
df2013.shape


# In[11]:


#Standardize country names 
df2013.loc[df2013['Country'] == 'USA', 'Country'] = 'United States'


# In[12]:


df2013 = df2013.rename(columns={'Account No': "id",
                                'Country':'Country',
                                'City Short Name': 'City',
                                'City Name' : 'Municipality',
                                'Reporting Year' : 'Year_report',
                                'Accounting Year': 'Date_measure',
                               #'Current Population': 'Population',
                               #'Gases included': 'Gases' ,
                               'Total City-wide Emissions (metric tonnes CO2e)': 'TotalEmissions',                                
                               #'Total Scope 1 Emissions (metric tonnes CO2e)': 'EmissionsScope1',
                               #'Total Scope 2 Emissions (metric tonnes CO2e)': 'EmissionsScope2',
                               #'Land area (in square km)': 'Land_Area',
                               #'Average altitude (m)': 'Altitude',
                               #"Average annual temperature (in Celsius)": 'Temperature',
                               #'City GDP' : 'GDP',
                               #'Increase/Decrease from last year': 'Reduction'
                               })


# In[13]:


#Extract year of emissions from "Accounting Year" into "EmissionYear"
date13 = df2013["Date_measure"].str.split(" - ", n = 1, expand = True)
df2013['Date_measure'] = pd.DatetimeIndex(date13[1]).year


# In[14]:


#Extract coordinates from "City Location" column into "Longitude" and "Latitude" columns 
df2013['Coords'] = df2013['City Location'].str.extract(r"\((.*?)\)", expand=False)

coord13 = df2013["Coords"].str.split(", ", n = 1, expand = True)
df2013["Longitude"]= coord13[1]
df2013["Latitude"]= coord13[0]


# In[15]:



df2013.drop(['C40', 'Country Location', 'Primary Methodology', 'Methodology Details', 
             'Reason for Increase/Decrease in Emissions', 'Further Information', 'City Location', 'Coords'], inplace=True, axis=1)


# In[16]:


df2013.columns


# In[17]:


#Drop all duplicate emissions data (some of the datasets slightly overlap)
df2013 = df2013.drop_duplicates(keep="first")#subset='TotalEmissions', 
df2013.shape


# ### CDP 2014 Dataset

# In[18]:


#Import CDP 2014 Dataset
df2014 = pd.read_csv("https://raw.githubusercontent.com/jadenio/CityEmissionsData/main/CDP%202012-2020/2014_-_Citywide_GHG_Emissions.csv")
df2014.shape


# In[19]:


#Standardize country names 
df2014.loc[df2014['Country'] == 'USA', 'Country'] = 'United States'


# In[20]:


#Rename columns
df2014 = df2014.rename(columns={'Account No': "id",
                                'Country':'Country',
                                'City Short Name': 'City',
                                'City Name' : 'Municipality',
                                'Reporting Year' : 'Year_report',
                                'Measurement Year': 'Date_measure',
                               #'Current Population': 'Population',
                               #'Gases included': 'Gases' ,
                               'Total City-wide Emissions (metric tonnes CO2e)': 'TotalEmissions',                                
                               #'Total Scope 1 Emissions (metric tonnes CO2e)': 'EmissionsScope1',
                               #'Total Scope 2 Emissions (metric tonnes CO2e)': 'EmissionsScope2',
                               #'Land area (in square km)': 'Land_Area',
                               #'Average altitude (m)': 'Altitude',
                               #"Average annual temperature (in Celsius)": 'Temperature',
                               #'City GDP' : 'GDP',
                               #'Increase/Decrease from last year': 'Reduction'
                               })


# In[21]:


#Extract coordinates from "City Location" column into "Longitude" and "Latitude" columns 
df2014['Coords'] = df2014['City Location'].str.extract(r"\((.*?)\)", expand=False)

coord14 = df2014["Coords"].str.split(", ", n = 1, expand = True)
df2014["Longitude"]= coord14[1]
df2014["Latitude"]= coord14[0]


# In[22]:



df2014.drop(['C40', 'Country Location', 'Primary Methodology', 'Methodology Details', 
             'Reason for Increase/Decrease in emissions', 'City Location', 'Country Location', 'Coords'], inplace=True, axis=1)


# In[23]:


df2014.columns


# In[24]:


#Drop all duplicate emissions data (some of the datasets slightly overlap)
df2014 = df2014.drop_duplicates(keep="first")#subset='TotalEmissions', 
df2014.shape


# ### CDP 2015 Dataset

# In[25]:


#Import CDP 2015 Dataset 
df2015 = pd.read_csv("https://raw.githubusercontent.com/jadenio/CityEmissionsData/main/CDP%202012-2020/2015_-_Citywide_Emissions.csv")
df2015.shape


# In[26]:


#Standardize country names 
df2015.loc[df2015['Country'] == 'USA', 'Country'] = 'United States'


# In[27]:


#Rename columns
df2015 = df2015.rename(columns={'Account No': "id",
                                'Country':'Country',
                                'City Short Name': 'City',
                                'City Name' : 'Municipality',
                                'Reporting Year' : 'Year_report',
                                'Measurement Year': 'Date_measure',
                               'Current Population': 'Population',
                               #'Gases included': 'Gases' ,
                               'Total City-wide Emissions (metric tonnes CO2e)': 'TotalEmissions',                                
                               #'Total Scope 1 Emissions (metric tonnes CO2e)': 'EmissionsScope1',
                               #'Total Scope 2 Emissions (metric tonnes CO2e)': 'EmissionsScope2',
                               #'Land area (in square km)': 'Land_Area',
                               #'Average altitude (m)': 'Altitude',
                               #"Average annual temperature (in Celsius)": 'Temperature',
                               #'City GDP' : 'GDP',
                               'Increase/Decrease from last year': 'Reduction'
                               })


# In[28]:


#Extract year of emissions from "Measurement Year" into "EmissionYear"
date15 = df2015["Date_measure"].str.split(" ", n = 1, expand = True)
df2015['Date_measure'] = pd.DatetimeIndex(date15[0]).year


# In[29]:


#Extract coordinates from "City Location" column into "Longitude" and "Latitude" columns 
df2015['Coords'] = df2015['City Location'].str.extract(r"\((.*?)\)", expand=False)

coord15 = df2015["Coords"].str.split(", ", n = 1, expand = True)
df2015["Longitude"]= coord15[1]
df2015["Latitude"]= coord15[0]


# In[30]:



df2015.drop(['C40', 'Country Location', 'Primary Methodology', 'Methodology Details', 
             'Reason for Increase/Decrease in emissions', 'City Location', 'Country Location', 'Coords'], inplace=True, axis=1)


# In[31]:


df2015.columns


# In[32]:


#Drop all duplicate emissions data (some of the datasets slightly overlap)
df2015 = df2015.drop_duplicates(keep="first")#subset='TotalEmissions', 
df2015.shape


# ### CDP 2016 Dataset

# In[33]:


#Import CDP 2016 Dataset
df2016 = pd.read_csv("https://raw.githubusercontent.com/jadenio/CityEmissionsData/main/CDP%202012-2020/2016_-_Citywide_GHG_Emissions.csv")
df2016.shape


# In[34]:


#Standardize country names 
df2016.loc[df2016['Country'] == 'USA', 'Country'] = 'United States'


# In[35]:


#Rename columns
df2016 = df2016.rename(columns={'Account Number': "id",
                                'Country':'Country',
                                'City Short Name': 'City',
                                'City Name' : 'Municipality',
                                'Reporting Year' : 'Year_report',
                                'Measurement Year': 'Date_measure',
                               'Current Population': 'Population',
                               'Gases included': 'Gases' ,
                               'Total City-wide Emissions (metric tonnes CO2e)': 'TotalEmissions',                                
                               'Total Scope 1 Emissions (metric tonnes CO2e)': 'EmissionsScope1',
                               'Total Scope 2 Emissions (metric tonnes CO2e)': 'EmissionsScope2',
                               '​Land area (in square km)': 'Land_Area',
                               'Average altitude (m)': 'Altitude',
                               "Average annual temperature (in Celsius)​": 'Temperature',
                               'City GDP' : 'GDP',
                               'Increase/Decrease from last year': 'Reduction'
                               })


# In[36]:


#Extract year of emissions from "Measurement Year" into "EmissionYear"
date16 = df2016["Date_measure"].str.split(" ", n = 1, expand = True)
df2016['Date_measure'] = pd.DatetimeIndex(date16[0]).year


# In[37]:


#Extract coordinates from "City Location" column into "Longitude" and "Latitude" columns 
df2016['Coords'] = df2016['City Location'].str.extract(r"\((.*?)\)", expand=False)

coord16 = df2016["Coords"].str.split(", ", n = 1, expand = True)
df2016["Longitude"]= coord16[1]
df2016["Latitude"]= coord16[0]


# In[38]:



df2016.drop(['C40', 'Country Location', 'Primary Methodology', 'Methodology Details', 
             'Reason for increase/decrease in emissions', 'Current Population Year',
             'GDP Currency', 'Year of GDP', 'GDP Source','Boundary',
             'City Location', 'Country Location', 'Coords'], inplace=True, axis=1)


# In[39]:


df2016.columns


# In[40]:


#Drop all duplicate emissions data (some of the datasets slightly overlap)
df2016 = df2016.drop_duplicates(keep="first")#subset='TotalEmissions', 
df2016.shape


# ### CDP 2017 Dataset

# In[41]:


#Import CDP 2017 Dataset
df2017 = pd.read_csv("https://raw.githubusercontent.com/jadenio/CityEmissionsData/main/CDP%202012-2020/2017_-_Cities_Community_Wide_Emissions.csv")
df2017.shape


# In[42]:


#Standardize country names 
df2017.loc[df2017['Country'] == 'USA', 'Country'] = 'United States'


# In[43]:


#Rename total emissions column to "TotalEmissions"
df2017 = df2017.rename(columns={'Account number': "id",
                                'Region':'Region',
                                'Country':'Country',
                                'City': 'City',
                                'Organization' : 'Municipality',
                                'Reporting year' : 'Year_report',
                                'Accounting year': 'Date_measure',
                               'Population': 'Population',
                               'Gases included': 'Gases' ,
                               'Total emissions (metric tonnes CO2e)': 'TotalEmissions',                                
                               'Total Scope 1 Emissions (metric tonnes CO2e)': 'EmissionsScope1',
                               'Total Scope 2 Emissions (metric tonnes CO2e)': 'EmissionsScope2',
                               '​Land area (in square km)': 'Land_Area',
                               '​Average altitude (m)': 'Altitude',
                               "Average annual temperature (in Celsius)​": 'Temperature',
                               'GDP' : 'GDP',
                               'Increase/Decrease from last year': 'Reduction'
                                })


# In[44]:


#Extract year of emissions from "Accounting Year" into "EmissionYear"
date17 = df2017["Date_measure"].str.split(" - ", n = 1, expand = True)
df2017['Date_measure'] = pd.DatetimeIndex(date17[1]).year


# In[45]:


#Extract coordinates from "City Location" column into "Longitude" and "Latitude" columns 
df2017['Coords'] = df2017['City Location'].str.extract(r"\((.*?)\)", expand=False)

coord17 = df2017["Coords"].str.split(", ", n = 1, expand = True)
df2017["Longitude"]= coord17[1]
df2017["Latitude"]= coord17[0]


# In[46]:



df2017.drop(['C40', 'Access','Country Location', 
             'Reason for increase/decrease in emissions', 
             'GDP Currency', 'GDP Year', 'GDP Source','Boundary','Protocol', 'Protocol column',
             'City Location', 'Country Location', 'Coords', 
            'Scopes Included ','Comment','Reason for increase/decrease in emissions',
            'Population year'], inplace=True, axis=1)


# In[47]:


df2017.columns


# In[48]:


#Drop all duplicate emissions data (some of the datasets slightly overlap)
df2017 = df2017.drop_duplicates(keep="first")#subset='TotalEmissions', 
df2017.shape


# ### CDP 2018-2019 Dataset

# In[49]:


df2018 = pd.read_csv("https://raw.githubusercontent.com/jadenio/CityEmissionsData/main/CDP%202012-2020/2018_-_2019_City-wide_Emissions.csv")
df2018.shape


# In[50]:


#Standardize country names 
df2018.loc[df2018['Country'] == 'United States of America', 'Country'] = 'United States'
df2018.loc[df2018['Country'] == 'Viet Nam', 'Country'] = 'Vietnam'


# In[51]:


#df2018.columns.values


# In[52]:


df2018 = df2018.rename(columns={'Account Number': "id",
                                'CDP Region':'Region',
                                'Country':'Country',
                                'City': 'City',
                                'Organization' : 'Municipality',
                                'Year Reported to CDP' : 'Year_report',
                                'Accounting Year': 'Date_measure',
                                'Population': 'Population',
                                'Gases Included': 'Gases',
                                'Total BASIC Emissions (GPC)': 'TotalEmissions',                                                                
                                'Total BASIC+ Emissions (GPC)': 'Total+Emissions',                                
                                'Total Scope 1 Emissions (metric tonnes CO2e)': 'EmissionsScope1',
                                'Total Scope 2 Emissions (metric tonnes CO2e)': 'EmissionsScope2',
                                'Total Scope 3 emissions (metric tonnes CO2e)': 'EmissionsScope3',
                                 'Direct emissions/ Scope 1 (metric tonnes CO2e) for Total generation of grid supplied energy\xa0': 'Direct_GenGridSuppEnergy',
                                 'Direct emissions/ Scope 1 (metric tonnes CO2e) for Total emissions (excluding generation of grid-supplied energy)\xa0': 'Direct_NonGenGridSuppEnergy',
                                 'Indirect emissions from use of grid supplied energy/Scope 2 (metric tonnes CO2e) for Total generation of grid supplied energy': 'Indirect_GenGridSuppEnergy',
                                 'Indirect emissions from use of grid supplied energy/Scope 2 (metric tonnes CO2e) for Total emissions (excluding generation of grid-supplied energy)': 'Indirect_NonGenGridSuppEnergy',
                                 'Emissions occurring outside city boundary/ Scope 3 (metric tonnes CO2e) for Total generation of grid supplied energy\xa0': 'Outside_GenGridSuppEnergy',
                                 'Emissions occurring outside city boundary/ Scope 3 (metric tonnes CO2e) for Total emissions (excluding generation of grid-supplied energy)\xa0':'Outside_NonGenGridSuppEnergy',
                               '​Land area (in square km)': 'Land_Area',
                               #'Average altitude (m)': 'Altitude',
                               #'Average annual temperature (in Celsius)'': 'Temperature',
                               #'GDP' : 'GDP',
                               'Chnage in emissions': 'Reduction',
                                'Direct emissions/ Scope 1 (metric tonnes CO2e) for Total generation of grid supplied energy ':'brr1'
                                })


# In[53]:


#Sum all Scope 1 and Scope 2 Emissions into "TotalEmissions"
#df2018["TotalEmissions"] = df2018.iloc[:,[15,16,17,18,21,22]].sum(axis=1)


# In[54]:


df2018['TotalEmissions'] = np.where(df2018['TotalEmissions'] == "Not Applicable", np.nan,df2018['TotalEmissions']).astype(float)
df2018['Total+Emissions'] = np.where(df2018['Total+Emissions'] == "Not Applicable", np.nan,df2018['Total+Emissions']).astype(float)


# In[55]:


#Extract year of emissions from "Accounting Year" into "EmissionYear"
date18 = df2018["Date_measure"].str.split(" - ", n = 1, expand = True)
df2018['Date_measure'] = pd.DatetimeIndex(date18[1]).year


# In[56]:


##Extract Coordinates into two columns, "Latitude" and "Longitude"
df2018['Coords'] = df2018['City Location'].str.extract(r"\((.*?)\)", expand=False)

coord18 = df2018["Coords"].str.split(" ", n = 1, expand = True)
df2018["Longitude"]= coord18[0]
df2018["Latitude"]= coord18[1]


# Add names of organization to city as an aproximation of city name in empty cases

# In[57]:


df2018['City'].fillna(df2018['Municipality'], inplace=True)


# In[58]:



df2018.drop(['Reporting Authority', 'Access','City-wide Emissions Inventory','Inventory Boundary',
             'Primary Protocol', 'Primary Protocol Comment', 
             'Common Reporting Framework inventory format (GPC)\xa0',
             'Reason for change','Population Year','City Location', 'Last update', 'Coords'
             
], inplace=True, axis=1)


# In[59]:


df2018.columns


# In[60]:


#Drop all duplicate emissions data (some of the datasets slightly overlap)
df2018 = df2018.drop_duplicates(keep="first")#subset='TotalEmissions', 
df2018.shape


# ### CDP 2019 Dataset
# 

# In[61]:


df2019 = pd.read_csv("https://raw.githubusercontent.com/jadenio/CityEmissionsData/main/CDP%202012-2020/2019_City-wide_Emissions.csv")
df2019.shape


# In[62]:


#Standardize country names 
df2019.loc[df2019['Country'] == 'United States of America', 'Country'] = 'United States'
df2019.loc[df2019['Country'] == 'United Kingdom of Great Britain and Northern Ireland', 'Country'] = 'United Kingdom'
df2019.loc[df2019['Country'] == 'Taiwan, Greater China', 'Country'] = 'Taiwan'
df2019.loc[df2019['Country'] == 'Viet Nam', 'Country'] = 'Vietnam'


# In[63]:


df2019 = df2019.rename(columns={'Account Number': "id",
                                'CDP Region':'Region',
                                'Country':'Country',
                                'City': 'City',
                                'Organization' : 'Municipality',
                                'Year Reported to CDP' : 'Year_report',
                                'Accounting Year': 'Date_measure',
                                'Population': 'Population',
                                'Gases Included': 'Gases' ,
                                'Total BASIC Emissions (GPC)': 'TotalEmissions',                                                                
                                'Total BASIC+ Emissions (GPC)': 'Total+Emissions',                                
                                'Total Scope 1 Emissions (metric tonnes CO2e)': 'EmissionsScope1',
                                'Total Scope 2 Emissions (metric tonnes CO2e)': 'EmissionsScope2',
                                'Total Scope 3 emissions (metric tonnes CO2e)': 'EmissionsScope3',
                                 'Direct emissions/ Scope 1 (metric tonnes CO2e) for Total generation of grid supplied energy\xa0': 'Direct_GenGridSuppEnergy',
                                 'Direct emissions/ Scope 1 (metric tonnes CO2e) for Total emissions (excluding generation of grid-supplied energy)\xa0': 'Direct_NonGenGridSuppEnergy',
                                 'Indirect emissions from use of grid supplied energy/Scope 2 (metric tonnes CO2e) for Total generation of grid supplied energy': 'Indirect_GenGridSuppEnergy',
                                 'Indirect emissions from use of grid supplied energy/Scope 2 (metric tonnes CO2e) for Total emissions (excluding generation of grid-supplied energy)': 'Indirect_NonGenGridSuppEnergy',
                                 'Emissions occurring outside city boundary/ Scope 3 (metric tonnes CO2e) for Total generation of grid supplied energy\xa0': 'Outside_GenGridSuppEnergy',
                                 'Emissions occurring outside city boundary/ Scope 3 (metric tonnes CO2e) for Total emissions (excluding generation of grid-supplied energy)\xa0':'Outside_NonGenGridSuppEnergy',
                                '\u200bLand area (in square km)': 'Land_Area',
                               #'Average altitude (m)': 'Altitude',
                               #"Average annual temperature (in Celsius)": 'Temperature',
                               #'GDP' : 'GDP',
                                'Chnage in emissions': 'Reduction'
                                })                            


# In[64]:


#Sum all Scope 1 Scope 2 and Scope 3 Emissions into column "TotalEmissions"
#df2019["TotalEmissions"] = df2019.loc[:,['Total Scope 1 Emissions (metric tonnes CO2e)',
#                                         'Total Scope 2 Emissions (metric tonnes CO2e)',
#                                         'Total Scope 3 emissions (metric tonnes CO2e)']].sum(axis=1)


# In[65]:


#Extract Emissions Year from "Measurement Year" into column "Accounting Year"
date19 = df2019["Date_measure"].str.split(" - ", n = 1, expand = True)
df2019['Date_measure'] = pd.DatetimeIndex(date19[1]).year


# In[66]:


##Extract Coordinates into two columns, "Latitude" and "Longitude"
df2019['Coords'] = df2019['City Location'].str.extract(r"\((.*?)\)", expand=False)

coord19 = df2019["Coords"].str.split(" ", n = 1, expand = True)
df2019["Longitude"]= coord19[0]
df2019["Latitude"]= coord19[1]


# In[67]:


df2019['City'].fillna(df2019['Municipality'], inplace=True)


# In[68]:


#df2018.loc[df2018["Longitude"].isna(), ['Country', 'City']]
#df2019.loc[df2019["City"].isna(), ['Country', 'Municipality','Year_report','City','City Location','Longitude','Latitude']]
#Some coordinate values are missing, these will be filled in manually


# In[69]:



df2019.drop(['Reporting Authority', 'Access','City-wide Emissions Inventory','Inventory Boundary',
             'Primary Protocol', 'Primary Protocol Comment', 
             'Common Reporting Framework inventory format (GPC)\xa0',
             'Reason for change','Population Year','City Location', 'Last update', 'Coords'
             
], inplace=True, axis=1)


# In[70]:


df2019.columns.values


# In[71]:


#Drop all duplicate emissions data (some of the datasets slightly overlap)
df2019 = df2019.drop_duplicates(keep="first")#subset='TotalEmissions', 
df2019.shape


# ### CDP 2020 Dataset

# In[72]:


#Import CDP 2020 Cities Emissions Dataset
df2020 = pd.read_csv("https://raw.githubusercontent.com/jadenio/CityEmissionsData/main/CDP%202012-2020/2020_-_City-Wide_Emissions.csv")
df2020.shape


# In[73]:


#Standardize country names 
df2020.loc[df2020['Country'] == 'United States of America', 'Country'] = 'United States'
df2020.loc[df2020['Country'] == 'United Kingdom of Great Britain and Northern Ireland','Country'] = 'United Kingdom'
df2020.loc[df2020['Country'] == 'Taiwan, Greater China','Country'] = 'Taiwan'
df2020.loc[df2020['Country'] == 'Viet Nam','Country'] = 'Vietnam'


# In[74]:


df2020 = df2020.rename(columns={'Account Number': "id",
                                'CDP Region':'Region',
                                'Country':'Country',
                                'City': 'City',
                                'Organization' : 'Municipality',
                                'Year Reported to CDP' : 'Year_report',
                                'Accounting year': 'Date_measure',
                               'Population': 'Population',
                               'Gases Included': 'Gases' ,
                               'TOTAL BASIC Emissions (GPC)': 'TotalEmissions',                                                                
                                'TOTAL BASIC+ Emissions (GPC)': 'Total+Emissions',                                
                                'TOTAL Scope 1 Emissions (metric tonnes CO2e)': 'EmissionsScope1',
                                'TOTAL Scope 2 emissions (metric tonnes CO2e)': 'EmissionsScope2',
                                'TOTAL Scope 3 Emissions': 'EmissionsScope3',
                                'Direct emissions (metric tonnes CO2e) for Total generation of grid-supplied energy': 'Direct_GenGridSuppEnergy',
                                 'Direct emissions (metric tonnes CO2e) for Total emissions (excluding generation of grid-supplied energy)': 'Direct_NonGenGridSuppEnergy',
                                 'Indirect emissions from use of grid supplied energy (metric tonnes CO2e) for Total generation of grid supplied energy': 'Indirect_GenGridSuppEnergy',
                                 'Indirect emissions from use of grid supplied energy (metric tonnes CO2e) for Total Emissions (excluding generation of grid-supplied energy)': 'Indirect_NonGenGridSuppEnergy',
                                 'Emissions occurring outside city boundary (metric tonnes CO2e) for Total Generation of grid supplied energy': 'Outside_GenGridSuppEnergy',
                                 'Emissions occurring outside city boundary (metric tonnes CO2e) for Total Emissions (excluding generation of grid-supplied energy)':'Outside_NonGenGridSuppEnergy',
                               'Land area (in square km)': 'Land_Area',
                               #'Average altitude (m)': 'Altitude',
                               #"Average annual temperature (in Celsius)": 'Temperature',
                               #'GDP' : 'GDP',
                               'Change in emissions': 'Reduction'
                                })   


# In[75]:


#Sum all Scope 1 and Scope 2 Emissions into column "TotalEmissions"
#df2020["TotalEmissions"] = df2020.loc[:,['TOTAL Scope 1 Emissions (metric tonnes CO2e)',
#                                         'TOTAL Scope 2 emissions (metric tonnes CO2e)',
#                                         'TOTAL Scope 3 Emissions']].sum(axis=1)


# In[76]:


#Extract Emissions Year from "MeasurementYear" into column "EmissionYear"
date2020 = df2020["Date_measure"].str.split(" - ", n = 1, expand = True)
df2020['Date_measure'] = pd.DatetimeIndex(date2020[1]).year


# In[77]:


##Extract Coordinates into two columns, "Latitude" and "Longitude"
df2020['Coords'] = df2020['City Location'].str.extract(r"\((.*?)\)", expand=False)

coord20 = df2020["Coords"].str.split(" ", n = 1, expand = True)
df2020["Longitude"]= coord20[0]
df2020["Latitude"]= coord20[1]


# In[78]:


df2020['City'].fillna(df2020['Municipality'], inplace=True)


# In[79]:


#df2020.loc[df2020["City"].isna(), ['Country', 'Municipality','Year_report','City','Longitude','Latitude']].sort_values(['Longitude'])
#No coordinates columns


# In[80]:



df2020.drop(['Access','City-wide emissions inventory','Administrative city boundary',
             'Inventory boundary (compared to Administrative city boundary)',
             'Primary Protocol', 'Primary Protocol Comment', 
             'Common Reporting Framework inventory format (GPC)',
             'Primary reason for the change in emissions','Population Year','City Location', 'Last update', 'Coords'             
            ], inplace=True, axis=1)


# In[81]:


df2020.columns.values


# In[82]:


#Drop all duplicate emissions data (some of the datasets slightly overlap)
df2020 = df2020.drop_duplicates(keep="first")#subset='TotalEmissions', 
df2020.shape


# ## Merging years datasets

# Merge datasets from 2012 to 2020

# In[83]:


#Create list of all datasets 
frames = [df2012, df2013, df2014, df2015, df2016, df2017, df2018, df2019, df2020]


# In[84]:


#Merge the datasets 
df = pd.concat(frames)


# In[85]:


df.columns


# In[86]:


df.shape


# In[87]:


pd.set_option('display.max_columns', None)
df


# Evaluate year to consider

# In[88]:


#Sort by account number and emissions year 
df.sort_values(by=['Country','Year_report'], inplace=True)


# In[89]:


pd.set_option('display.float_format', lambda x: '%.1f' % x)
df.pivot_table(index =['Date_measure'], 
                     columns = 'Year_report', 
                     values = 'TotalEmissions', 
                     aggfunc = max).reset_index()


# In[90]:


df = df.rename(columns={'Country': "Country Name",'Year_report': "Year"})


# Recode categorical variables

# In[91]:


df['Reduction2'] = np.where(df['Reduction'].isin(["Other: No change","Stayed the same"]), "No change",
                  np.where(df['Reduction'].isin(["Other: This is our first year of estimation","This is our first year of calculation"]), "First calculation",
                                             np.where(df['Reduction'].isin(["Decreased"]), "Decreased",
                                                      np.where(df['Reduction'].isin(["Increased"]), "Increased",
                           'No Information'))))
df['Reduction2'].value_counts()
df.pivot_table(index =['Reduction'], 
                     columns = 'Reduction2', 
                     values = 'TotalEmissions', 
                     aggfunc = len).reset_index()


# In[92]:


df['Gas_CH4'] = np.where(df['Gases'].str.contains("CH4|GPC gases"), 1,0)
df['Gas_CO2'] = np.where(df['Gases'].str.contains("CO2|GPC gases"), 1,0)
df['Gas_N20'] = np.where(df['Gases'].str.contains("N20|GPC gases"), 1,0)
df['Gas_HFCs'] = np.where(df['Gases'].str.contains("HFCs|GPC gases"), 1,0)
df['Gas_NF3'] = np.where(df['Gases'].str.contains("NF3|GPC gases"), 1,0)
df['Gas_PFCs'] = np.where(df['Gases'].str.contains("PFCs|GPC gases"), 1,0)
df['Gas_SF6'] = np.where(df['Gases'].str.contains("SF6|GPC gases"), 1,0)


# Standardize country names to find Country codes

# In[93]:


#Standardize country names 
df.loc[df['Country Name'] == 'Taiwan, Greater China', 'Country Name'] = 'Taiwan, Province of China'
df.loc[df['Country Name'] == 'South Korea', 'Country Name'] = 'Korea, Republic of'
df.loc[df['Country Name'] == 'China, Hong Kong Special Administrative Region', 'Country Name'] = 'Hong Kong Special Administrative Region of China'
df.loc[df['Country Name'] == 'Bolivia (Plurinational State of)', 'Country Name'] = 'Bolivia'
df.loc[df['Country Name'] == 'Democratic Republic of the Congo', 'Country Name'] = 'Congo, The Democratic Republic of the'
df.loc[df['Country Name'] == 'Venezuela (Bolivarian Republic of)', 'Country Name'] = 'Venezuela'


# In[94]:


df['Country Code'] = df['Country Name'].apply(lambda x: do_fuzzy_search(x))


# In[95]:


df[df['Country Code'].isna()]['Country Name'].value_counts()


# Standardize country names after codes are found

# In[96]:


df.loc[df['Country Name'] == 'Hong Kong Special Administrative Region of China', 'Country Name'] = 'Hong Kong'
df.loc[df['Country Name'] == 'Taiwan, Province of China', 'Country Name'] = 'Taiwan'
df.loc[df['Country Name'] == 'United Kingdom of Great Britain and Northern Ireland', 'Country Name'] = 'United Kingdom'
df.loc[df['Country Name'] == 'Russia', 'Country Name'] = 'Russian Federation'


# In[97]:


#pycountry.countries.search_fuzzy('Hong Kong')


# Identify missing values in id variables

# In[98]:


#df[df['id'].isna()]['Country Name'].value_counts()


# In[99]:


df.shape


# In[100]:


df.info()


# Evaluate country and city names

# In[101]:


pd.set_option('display.max_rows', None)
pd.crosstab([df['Country Code'],df['Country Name']],df['Year'])


# Normalize city names

# In[102]:


df['CityOld'] = df['City']


# remove accents in city names

# In[103]:


df['City'] = df['City'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


# remove punctuations

# In[104]:


df['City'] = df['City'].str.replace(r'[^\w\s]+', '')


# Remove strings from organization column copied to city name

# In[105]:


stringstoremove = ['Municipality', 'Municipalidad', 'Municipio', 
                   'Metropolitana', 'Metropolitano', 'Metropolitan', 'metropole',
                   'Communaute urbaine du', 'Comune di', 'Commune', 
                   'Alcaldia', 'Municipal','Concejo', 
                   'Kommune', 'Kommun', 'kommune',
                   'Ayuntamiento', 
                   'Distrito', 'Distrital', 'District', 
                   'Landeshauptstadt', 'Stadt', 
                   'Medio Ambiente', 'la Region Norte', 'para la gestion integral',  'Junta Intermunicipal',
                   'People\'s', 'Sub-',
                   'Combined Authority', 
                   'Council', 
                   'Corporation', 
                   'Prefeitura',  'Local', 'Town', 
                   'Provincial', 'City', 'Regency', 
                   'Governments', 'Government', 'Gobierno', 
                   'County', 'Authority', 'Region',
                   ' the ', ' of ', ' de ', ' del ']
df['City'] =  df['City'].str.replace('|'.join(stringstoremove), '') 


# remove trailing blanks

# In[106]:


df['City'] = df['City'].map(lambda x: x.strip())


# adjust specific city names

# In[107]:


df.loc[df['City'] == 'Ceres (Argentina)', 'City'] = 'Ceres'
df.loc[df['City'] == 'Oliva (Argentina)', 'City'] = 'Oliva'
df.loc[df['City'] == 'San Isidro (Argentina)', 'City'] = 'San Isidro'
df.loc[df['City'] == 'Santa Anita (Argentina)', 'City'] = 'Santa Anita'
df.loc[df['City'] == 'La Paz (Bolivia)', 'City'] = 'La Paz'
df.loc[df['City'] == 'St Catharines ON', 'City'] = 'St Catharines'
df.loc[df['City'] == 'Madrid (Colombia)', 'City'] = 'Madrid'
df.loc[df['City'] == 'Santa Ana (Costa Rica)', 'City'] = 'Santa Ana'
df.loc[df['City'] == 'Santa Barbara (Costa Rica)', 'City'] = 'Santa Barbara'
df.loc[df['City'] == 'Grand Nancy', 'City'] = 'Nancy'
df.loc[df['City'] == 'Nice Cote dAzur', 'City'] = 'Nice'
df.loc[df['City'] == 'Greater London', 'City'] = 'London'
df.loc[df['City'] == 'Rome', 'City'] = 'Roma'
df.loc[df['City'] == 'Venice', 'City'] = 'Venezia'
df.loc[df['City'] == 'Alton IL', 'City'] = 'Alton'
df.loc[df['City'] == 'Arlington VA', 'City'] = 'Arlington'
df.loc[df['City'] == 'Aspen and Pitkin County', 'City'] = 'Aspen'
df.loc[df['City'] == 'Cambridge', 'City'] = 'Cambridge MA'
df.loc[df['City'] == 'Charlottesville, VA', 'City'] = 'Charlottesville'
df.loc[df['City'] == 'Denton TX', 'City'] = 'Denton'
df.loc[df['City'] == 'Durham', 'City'] = 'Durham NC'
df.loc[df['City'] == 'Easton PA', 'City'] = 'Easton'
df.loc[df['City'] == 'Emeryville CA', 'City'] = 'Emeryville'
df.loc[df['City'] == 'Fayetteville AR', 'City'] = 'Fayetteville'
df.loc[df['City'] == 'Lexington', 'City'] = 'Lexington MA'
df.loc[df['City'] == 'Miami Beach FL', 'City'] = 'Miami Beach'
df.loc[df['City'] == 'Nashville and Davidson', 'City'] = 'Nashville'
df.loc[df['City'] == 'San Leandro CA', 'City'] = 'San Leandro'
df.loc[df['City'] == 'Somerville MA', 'City'] = 'Somerville'
df.loc[df['City'] == 'Tempe AZ', 'City'] = 'Tempe'
df.loc[df['City'] == 'Pretoria', 'City'] = 'Pretoria Tshwane'


# Fill missing values in coordinates using similar city names, and regions

# In[108]:


df['Longitude'] = df.groupby(["Country Code","id"])['Longitude'].transform('last')
df['Latitude'] = df.groupby(["Country Code","id"])['Latitude'].transform('last')
df['Region'] = df.groupby(["Country Code"])['Region'].transform('last')


# In[109]:


df['Region'] = np.where(df['Country Code'] == "IRL", "Europe", df['Region'] )
df['Region'] = np.where(df['Country Code'] == "KOR", "East Asia", df['Region'] )


# Remove duplicated rows with 0 emissions, sorting increasing emissions and keeping last duplicated row (mainly 2019)

# In[110]:


df.sort_values(['Country Name', 'Country Code', 'City', 'id', 'Year', 'TotalEmissions'], inplace=True)


# In[111]:


df = df.drop_duplicates(subset = ['Country Name', 'Country Code', 'City', 'Year','id'], 
                                    keep="last") 
df.shape


# In[112]:


#Keep only observations that have at least Emissions Data
df['TotalEmissions'] = df['TotalEmissions'].replace(0, np.nan)
df = df[df['TotalEmissions'].notna()]


# In[113]:


pd.crosstab([df['Country Code'],df['Country Name'],df['City']],df['Year'])


# In[114]:


df.head(5)


# ## Save data to csv

# Select and rename final columns

# In[115]:


#reorder columns to add prefix
Ind3 = Ind2 + ['Region', 'Municipality', 'id', 'Date_measure', 'Latitude', 'Longitude', 'Altitude']
Char = ['GDP', 'Land_Area', 'Population', 'Temperature']
Emiss = ['EmissionsScope1', 'EmissionsScope2', 'EmissionsScope3', 'TotalEmissions', 'Total+Emissions',
         'Direct_GenGridSuppEnergy','Direct_NonGenGridSuppEnergy', 
         'Indirect_GenGridSuppEnergy', 'Indirect_NonGenGridSuppEnergy', 
         'Outside_GenGridSuppEnergy', 'Outside_NonGenGridSuppEnergy',
        'Gas_CH4', 'Gas_CO2', 'Gas_N20', 'Gas_HFCs', 'Gas_NF3',
       'Gas_PFCs', 'Gas_SF6', 'Reduction2']
Column_names = Ind3 + Char + Emiss
CDPFinal = df[Column_names]
#df.columns[~df.columns.isin(CDPFinal.columns)]


# In[116]:


#rename not identification columns
newnames = "CDP_" + CDPFinal.columns[~CDPFinal.columns.isin(Ind2)]
CDPFinal.columns = Ind2 + newnames.tolist()
CDPFinal.columns


# In[117]:


CDPFinal = CDPFinal.set_index(['Country Code', 'City', 'Year'])


# In[118]:


#Export cleaned data to csv file
CDPFinal.to_csv('../data/02_output/00_CDP_Clean.csv')


# In[ ]:





# This is part second code, it will process all external datasets and create one consolidated with main information to be used in the future models.

# In[1]:


# modules to use
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pycountry
import functools
import re


# In[2]:


#!pip install pycountry


# In[3]:


# method to identify country code based on country name
@functools.lru_cache(None)
def do_fuzzy_search(country):
    try:   
        result = pycountry.countries.search_fuzzy(country)
    except Exception:
        return np.nan
    else:
        return result[0].alpha_3


# In[4]:


# fix indexes
Ind = ['Country Name', 'Country Code', 'Year'] 
Ind2 = ['Country Name', 'Country Code', 'City','Year'] 


# # Others sources

# ## Gini indicator
# https://data.worldbank.org/indicator/SI.POV.GINI

# In[5]:


GINI_df = pd.read_csv('../data/01_input/00_GINI.csv', header=2, encoding='utf-8')


# In[6]:


GINI_df.columns


# In[7]:


col_list = ["Country Name", "Country Code", "Indicator Code"]+ [str(x) for x in range(2012,2020)]
GINI_df = pd.DataFrame(GINI_df, columns = col_list)


# In[8]:


#years as column
GINI_df = GINI_df.melt(id_vars=["Country Name", "Country Code", "Indicator Code"], 
        var_name="Year", 
        value_name="GINI")
GINI_df.head(5)


# In[9]:


GINI_df.info()


# In[10]:


GINI_df['Year'] = pd.to_numeric(GINI_df['Year'])
GINI_df['Year'].value_counts()


# In[11]:


GINI_df['Indicator Code'].value_counts()


# In[12]:


GINI_df[GINI_df['Country Code'].isna()]['Country Name'].value_counts()


# In[13]:


GINI_df = pd.DataFrame(GINI_df, columns = ['Country Name', "Country Code", "Year", "GINI"])


# In[14]:


#rename not identification columns
newnames = "GINI_" + GINI_df.columns[~GINI_df.columns.isin(Ind)]
GINI_df.columns = Ind + newnames.tolist()


# In[15]:


GINI_df


# ## Population
# https://data.worldbank.org/indicator/SP.URB.TOTL.IN.ZS

# In[16]:


Population_df = pd.read_csv('../data/01_input/00_Population.csv', skiprows=4,encoding='utf-8')
Population_df.columns


# In[17]:


col_list = ["Country Name", "Country Code", "Indicator Code"]+ [str(x) for x in range(2012,2020)]
Population_df = pd.DataFrame(Population_df, columns = col_list)


# In[18]:


#years as column
Population_df = Population_df.melt(id_vars=["Country Name", "Country Code", "Indicator Code"], 
        var_name="Year", 
        value_name="Population")
Population_df.head(5)


# In[19]:


Population_df['Year'] = pd.to_numeric(Population_df['Year'])
Population_df['Year'].value_counts()
#Population_df.info()


# In[20]:


Population_df['Indicator Code'].value_counts()


# In[21]:


Population_df[Population_df['Country Code'].isna()]['Country Name'].value_counts()


# In[22]:


Population_df = pd.DataFrame(Population_df, columns = ['Country Name', "Country Code", "Year", "Population"])


# In[23]:


#rename not identification columns
newnames = "POP_" + Population_df.columns[~Population_df.columns.isin(Ind)]
Population_df.columns = Ind + newnames.tolist()


# In[24]:


Population_df


# ## GDP indicator
# https://www.imf.org/external/pubs/ft/weo/disclaim.htm

# In[25]:


GDP_df = pd.read_csv('../data/01_input/00_GDP.csv', encoding='utf-8')
GDP_df.columns


# In[26]:


GDP_df.info()


# In[27]:


GDP_df = GDP_df[GDP_df['Index Year'] >= 2012]
GDP_df['Index Year'].value_counts()


# In[28]:


GDP_df = GDP_df.rename(
    columns={
        "Name": "Country Name",
        "Index Year": "Year",
        "Overall Score": "GDP"})


# In[29]:


#replace special country names not found
GDP_df.loc[GDP_df['Country Name'] == "Laos", 'Country Name'] = "Lao People's Democratic Republic"
GDP_df.loc[GDP_df['Country Name'] == "Burma", 'Country Name'] = "Myanmar"
GDP_df.loc[GDP_df['Country Name'] == "North Korea", 'Country Name'] = "Democratic People's Republic of Korea"
GDP_df.loc[GDP_df['Country Name'] == "South Korea", 'Country Name'] = "Republic of Korea"
GDP_df.loc[GDP_df['Country Name'] == "Democratic Republic of Congo", 'Country Name'] = "Congo, The Democratic Republic of the"
GDP_df.loc[GDP_df['Country Name'] == "Republic of Congo", 'Country Name'] = "Republic of the Congo"
GDP_df.loc[GDP_df['Country Name'] == "Macau", 'Country Name'] = "Macao"


# In[30]:


#Add country code
GDP_df['Country Code'] = GDP_df['Country Name'].apply(lambda x: do_fuzzy_search(x))


# In[31]:


GDP_df[GDP_df['Country Code'].isna()]['Country Name'].value_counts()


# In[32]:


#reorder columns to add prefix
Column_names = Ind + GDP_df.columns[~GDP_df.columns.isin(Ind)].tolist()
GDP_df = GDP_df[Column_names]
GDP_df.columns


# In[33]:


#rename not identification columns
newnames = "GDP_" + GDP_df.columns[~GDP_df.columns.isin(Ind)]
GDP_df.columns = Ind + newnames.tolist()


# In[34]:


GDP_df


# ## HDI 

# See Technical note 1 at http://hdr.undp.org/sites/default/files/hdr2020_technical_notes.pdf for details on how the HDI is calculated.

# In[35]:


HDI_df = pd.read_csv('../data/01_input/00_HDI.csv', skiprows=5, skipfooter=17, encoding='utf-8', 
                     na_values="..", engine = "python")


# In[36]:


col_list = ["Country", "HDI Rank"]+ [str(x) for x in range(1990,2019)]
HDI_df = pd.DataFrame(HDI_df, columns = col_list)
#HDI_df.columns


# In[37]:


#years as column
HDI_df = HDI_df.melt(id_vars=["Country", "HDI Rank"], 
        var_name="Year", 
        value_name="HDI")


# In[38]:


HDI_df.info()


# In[39]:


HDI_df['Year'] = pd.to_numeric(HDI_df['Year'])


# In[40]:


HDI_df = HDI_df.rename(
    columns={"Country": "Country Name"})


# In[41]:


#delete country names parentheses
HDI_df['Country Name'] = HDI_df['Country Name'].str.replace(r"\(.*\)","")


# In[42]:


#remove trailing blanks
HDI_df['Country Name'] = HDI_df['Country Name'].map(lambda x: x.strip())


# In[43]:


#replace special country names not found
HDI_df.loc[HDI_df['Country Name'].str.contains("Hong Kong, China"), 'Country Name'] = "Hong Kong Special Administrative Region of China"
HDI_df.loc[HDI_df['Country Name'].str.contains("d'Ivoire"), 'Country Name'] = "Republic of Côte d'Ivoire"


# In[44]:


HDI_df['Country Code'] = HDI_df['Country Name'].apply(lambda x: do_fuzzy_search(x))


# In[45]:


HDI_df[HDI_df['Country Code'].isna()]['Country Name'].value_counts()


# In[46]:


#reorder columns to add prefix
Column_names = Ind + HDI_df.columns[~HDI_df.columns.isin(Ind)].tolist()
HDI_df = HDI_df[Column_names]
HDI_df.columns


# In[47]:


#rename not identification columns
newnames = "HDI_" + HDI_df.columns[~HDI_df.columns.isin(Ind)]
HDI_df.columns = Ind + newnames.tolist()


# In[48]:


HDI_df.head(5)


# ## Our world in data 

# https://ourworldindata.org/co2-and-other-greenhouse-gas-emissions

# https://github.com/owid/co2-data

# In[49]:


owid_df = pd.read_csv('../data/01_input/00_owid.csv', encoding='utf-8')
owid_df.columns


# In[50]:


owid_df = owid_df.rename(
    columns={"country": "Country Name",
            "year": "Year"})


# In[51]:


#owid_df['Year'].value_counts()


# In[52]:


owid_df = owid_df[owid_df['Year'].isin([str(x) for x in range(2012,2019)])]
#owid_df['Year'].value_counts()


# In[53]:


#owid_df[owid_df['iso_code'].isna()]['Country Name'].value_counts()


# In[54]:


regna = ["EU-28", "EU-27", "South America", "Europe (excl. EU-28)", "Africa", "International transport", "World",
        "Europe", "Asia", "Oceania", "Asia (excl. China & India)", "Europe (excl. EU-27)", "North America", "North America (excl. USA)"]
owid_df = owid_df[~owid_df['Country Name'].isin(regna)]


# In[55]:


#pycountry.countries.search_fuzzy("Micronesia")


# In[56]:


#replace special country names not found
owid_df.loc[owid_df['Country Name'].str.contains("Macao"), 'Country Name'] = "Macao Special Administrative Region of China"
owid_df.loc[owid_df['Country Name'] == "Laos", 'Country Name'] = "Lao People's Democratic Republic"
owid_df.loc[owid_df['Country Name'] == "North Korea", 'Country Name'] = "Democratic People's Republic of Korea"
owid_df.loc[owid_df['Country Name'] == "South Korea", 'Country Name'] = "Republic of Korea"
owid_df.loc[owid_df['Country Name'] == "Democratic Republic of Congo", 'Country Name'] = "Congo, The Democratic Republic of the"
owid_df.loc[owid_df['Country Name'] == "Republic of Congo", 'Country Name'] = "Republic of the Congo"
owid_df.loc[owid_df['Country Name'] == "Cape Verde", 'Country Name'] = "Cabo Verde"
owid_df.loc[owid_df['Country Name'] == "Faeroe Islands", 'Country Name'] = "Faroe Islands"
owid_df.loc[owid_df['Country Name'].str.contains("Wallis and Futuna Islands"), 'Country Name'] = "Wallis and Futuna"
owid_df.loc[owid_df['Country Name'].str.contains("Kuwaiti Oil Fires"), 'Country Name'] = "State of Kuwait"
owid_df.loc[owid_df['Country Name'].str.contains("Bonaire Sint Eustatius and Saba"), 'Country Name'] = "Bonaire, Sint Eustatius and Saba"


# In[57]:


owid_df['Country Code'] = owid_df['Country Name'].apply(lambda x: do_fuzzy_search(x))


# In[58]:


owid_df[owid_df['Country Code'].isna()]['Country Name'].value_counts()


# In[59]:


#reorder columns to add prefix
Column_names = Ind + owid_df.columns[~owid_df.columns.isin(Ind)].tolist()
owid_df = owid_df[Column_names]
owid_df.columns


# In[60]:


#rename not identification columns
newnames = "OWID_" + owid_df.columns[~owid_df.columns.isin(Ind)]
owid_df.columns = Ind + newnames.tolist()


# In[61]:


owid_df4 = owid_df.drop('OWID_iso_code', axis = 1)
owid_df4.head(5)


# ## Temperature data by city

# In[63]:


weather_df = pd.read_csv('../data/01_input/00_weather.csv', sep =",", na_values=-99.0)


# In[64]:


weather_df = weather_df.rename(
    columns={"Country": "Country Name",
            "Country_Code": "Country Code"})


# In[65]:


#weather_df[weather_df['City'].str.contains("Brussels")]


# In[66]:


#Summarizes temperatures by year
weathYear_df = weather_df.groupby(['Country Code', 'Country Name', 'City', 'Year']).agg({'AvgTemperature': lambda x: x.mean(skipna=True)}).reset_index()


# In[67]:


weathYear_df = weathYear_df[weathYear_df['Year'].isin([str(x) for x in range(2012,2019)])]
#weathYear_df['Year'].value_counts()


# In[68]:


weathYear_df[weathYear_df['Country Code'].isna()]['Country Name'].value_counts()


# In[69]:


#reorder columns to add prefix
Column_names = Ind2 + weathYear_df.columns[~weathYear_df.columns.isin(Ind2)].tolist()
weathYear_df = weathYear_df[Column_names]
weathYear_df.columns


# In[70]:


#rename not identification columns
newnames = "Temp_" + weathYear_df.columns[~weathYear_df.columns.isin(Ind2)]
weathYear_df.columns = Ind2 + newnames.tolist()
weathYear_df.head(5)


# # Consolidation of external sources

# In[71]:


#datasets by country
GINI_df2 = GINI_df.set_index(['Country Code', 'Year'])
Population_df2 = Population_df.set_index(['Country Code', 'Year'])
GDP_df2 = GDP_df.set_index(['Country Code', 'Year'])
HDI_df2 = HDI_df.set_index(['Country Code', 'Year'])
owid_df2 = owid_df.set_index(['Country Code', 'Year'])
#datasets by city
weathYear_df2 = weathYear_df.set_index(['Country Code', 'City','Year'])


# In[72]:


GINI_df2.info()


# In[73]:


Population_df2.info()


# In[74]:


GDP_df2.info()


# In[75]:


HDI_df2.info()


# In[76]:


owid_df2.info()


# In[77]:


weathYear_df2.info()


# In[78]:


from functools import reduce
data_frames = [owid_df2, GINI_df2, 
               Population_df2, GDP_df2, HDI_df2]
External = reduce(lambda  left, right: pd.merge(left, right, on=['Country Code', 'Year','Country Name'],
                                            how='outer'), data_frames)

External.head(5)


# In[79]:


External2 = weathYear_df2             


# In[80]:


#weathYear_df2[weathYear_df2.index.get_level_values('City').str.contains(['Albania'])]
#land_df2[land_df2.index.get_level_values('City').str.contains('Alban')]


# In[81]:


#Export cleaned data to csv file
External.to_csv('../data/02_output/00_ExternalCountry_Clean.csv')


# In[82]:


External2.to_csv('../data/02_output/00_ExternalCity_Clean.csv')


# In[ ]:





# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Merging-dataset-by-country,-year-and-cities" data-toc-modified-id="Merging-dataset-by-country,-year-and-cities-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Merging dataset by country, year and cities</a></span></li><li><span><a href="#Summarize-gas-emissions-by-cities" data-toc-modified-id="Summarize-gas-emissions-by-cities-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Summarize gas emissions by cities</a></span></li></ul></div>

# In[1]:


#Import required packages
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pycountry
import functools
import re


# ## Merging dataset by country, year and cities

# In[2]:


#Import CDP Clean Cities Emissions Dataset
CDP_df = pd.read_csv("../data/02_output/00_CDP_Clean.csv")


# In[3]:


#Import External Clean Dataset 
EXT1_df = pd.read_csv("../data/02_output/00_ExternalCountry_Clean.csv")
EXT2_df = pd.read_csv("../data/02_output/00_ExternalCity_Clean.csv")


# In[4]:


CDP_df.info()


# In[5]:


EXT1_df.info()


# In[6]:


EXT2_df.info()


# Only cases with Emissions are keep, and country information is add to this tuples

# In[7]:


Main1_df = CDP_df.merge(EXT1_df, how = 'left', on = ['Country Code', 'Year', 'Country Name'])
Main1_df.shape
#Main1_df.head()


# All tuples from EXT2 are merged with Emissions in order to have information from cities even if the year dont have information in emissions

# In[8]:


Main2_df = Main1_df.merge(EXT2_df, how = 'left', on = ['Country Code', 'Year', 'City', 'Country Name'])
Main2_df.shape
#Main2_df.head()


# In[9]:


#Main2_df = Main2_df.set_index(['Country Code', 'City', 'Year'])


# In[10]:


Main2_df[Main2_df['City'].str.contains("Abington")]


# Compare equal variables from different sources and fill if necessary

# In[11]:


#Main2_df[['OWID_gdp','GDP_GDP']].isna().sum()/len(Main2_df)
Main2_df[['OWID_population','POP_Population']].isna().sum()/len(Main2_df)


# In[12]:


Main2_df[['Country Name', 'City','Year','OWID_gdp','GDP_GDP']]
Main2_df[['Country Name', 'City','Year','OWID_population','POP_Population']]


# In[13]:


Main2_df.drop(['OWID_iso_code', 'OWID_gdp', 'OWID_population','HDI_HDI Rank'], axis = 1, inplace = True)


# In[14]:


Main2_df.columns


# ## Summarize gas emissions by cities
# 
# The year percentage of change was calculated for each city using the pct_change function  
# 
# pct_change = $\frac{(A_1 - A_0)}{A_0}$ 
# 
# When no more than one year is found pct_change was fixed to 0 (no change).  
# Positive values means a increment in gas emission, 0 means no movement and negative values means reduction

# In[15]:


pd.set_option('display.float_format', lambda x: '%.1f' % x)
Main2_df.pivot_table(index =['Country Code', 'Country Name'], 
                     columns = 'Year', 
                     values = 'CDP_TotalEmissions', 
                     aggfunc = max).reset_index()


# In[16]:


#pd.set_option('display.max_rows', None)
Main2_df['CDP_pct_change'] = Main2_df.groupby(['Country Code','City'])['CDP_TotalEmissions'].pct_change()
Main2_df['CDP_pct_change'].fillna(0,inplace = True)


# In[17]:


Main2_df.dtypes
#CDPFinal


# In[18]:


get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib
import matplotlib.pyplot as plt

fig1, ax = plt.subplots(figsize=(5, 3))
ax.scatter(x=Main2_df['CDP_TotalEmissions'], 
            y=Main2_df['CDP_pct_change'], 
            marker='o', c='r', edgecolor='b')
ax.set_title('Scatter: TotalEmissions versus pct_change')
ax.set_xlabel('TotalEmissions')
ax.set_ylabel('pct_change')
#ax.set_xlim(xmin=0, xmax=5000000)
#ax.set_ylim(ymin=-5, ymax=5)

for i, txt in enumerate(Main2_df['City']):
    ax.annotate(txt, (Main2_df['CDP_TotalEmissions'][i], Main2_df['CDP_pct_change'][i]))


ax.annotate('Report Inconsistencies', xy=(50000000, 800000), xytext=(100000000, 800000),
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="angle3,angleA=45,angleB=-45"))


# Inconsistent values in TotalEmissions, when change in percentage is greater than 5 or lower than -5, values were removed and marked in the inconsistent column

# In[19]:


Main2_df['CDP_inconsistent'] = np.where((Main2_df['CDP_pct_change'] > 5) | (Main2_df['CDP_pct_change'] < -5) , 
                                1, 0)

Main2_df['CDP_pct_change2'] = np.where((Main2_df['CDP_pct_change'] > 5) | (Main2_df['CDP_pct_change'] < -5),
                              np.nan, Main2_df['CDP_pct_change'])

Main2_df['CDP_TotalEmissions'] = np.where((Main2_df['CDP_pct_change'] > 5) | (Main2_df['CDP_pct_change'] < -5),
                              np.nan, Main2_df['CDP_TotalEmissions'])

Main2_df.drop('CDP_pct_change', axis = 1, inplace = True)


# In[20]:


#Reduced_df[Reduced_df['City'] == "Abington"]
Main2_df = Main2_df[Main2_df['CDP_TotalEmissions'].notna()]
Main2_df.shape


# In[21]:


pd.set_option('display.max_rows', None)
missing1 = Main2_df.isna().sum()/len(Main2_df)
missing1.sort_values(ascending=False).reset_index()


# In[22]:


Main2_df.drop(['Temp_AvgTemperature','CDP_Total+Emissions','CDP_EmissionsScope3',
                 'CDP_Outside_GenGridSuppEnergy', 'CDP_Indirect_GenGridSuppEnergy',
                 'CDP_Direct_GenGridSuppEnergy','CDP_Outside_NonGenGridSuppEnergy',
                 'CDP_Indirect_NonGenGridSuppEnergy','CDP_Direct_NonGenGridSuppEnergy'], axis = 1, inplace = True)


# In[29]:


Main2_df.shape


# In[23]:


#Export cleaned data to csv file
Main2_df.to_csv('../data/02_output/01_DataToPreProcYear.csv')


# Values are summarize to have one value by city, using the mean of all available years for all columns

# In[24]:


Reduced_df = Main2_df.groupby(['Country Code','Country Name','City','CDP_id']).mean().reset_index()
Reduced_df.drop(['Year','CDP_Date_measure'], axis = 1, inplace = True)
Reduced_df.shape


# add last year of emissions reported

# In[25]:


Reduced2_df = Main2_df.groupby(['Country Code','Country Name','City','CDP_id']).max().reset_index()
Reduced2_df = Reduced2_df[['Country Code','Country Name','City','CDP_id','CDP_Date_measure']]


# In[26]:


Reduced_df = Reduced_df.merge(Reduced2_df, how = 'left', on = ['Country Code','Country Name','City','CDP_id'])
Reduced_df.shape


# In[27]:


pd.set_option('display.max_rows', None)
missing = Reduced_df.isna().sum()/len(Reduced_df)
missing.sort_values(ascending=False).reset_index()


# In[28]:


#Export cleaned data to csv file
Reduced_df.to_csv('../data/02_output/01_DataToPreProc.csv')


# In[ ]:





# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Data-by-city" data-toc-modified-id="Data-by-city-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Data by city</a></span><ul class="toc-item"><li><span><a href="#Detection-of-outliers" data-toc-modified-id="Detection-of-outliers-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Detection of outliers</a></span></li><li><span><a href="#Creation-of-response-variable" data-toc-modified-id="Creation-of-response-variable-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Creation of response variable</a></span></li><li><span><a href="#Drop-columns-with-missing-values" data-toc-modified-id="Drop-columns-with-missing-values-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Drop columns with missing values</a></span></li></ul></li><li><span><a href="#Data-by-year-city" data-toc-modified-id="Data-by-year-city-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Data by year city</a></span><ul class="toc-item"><li><span><a href="#Detection-of-outliers" data-toc-modified-id="Detection-of-outliers-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Detection of outliers</a></span></li><li><span><a href="#Creation-of-response-variable" data-toc-modified-id="Creation-of-response-variable-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>Creation of response variable</a></span></li></ul></li></ul></div>

# In[1]:


import sklearn as sk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


pd.set_option('display.float_format', lambda x: '%.3f' % x)


# In[3]:


pd.set_option('display.max_rows', None)


# ## Data by city

# In[4]:


data = pd.read_csv('../data/02_output/01_DataToPreProc.csv', sep=',', index_col = ['Unnamed: 0'])
data['City'] = data['City'].str.strip()
print(data.shape,data.columns.values)
data


# ### Detection of outliers

# In[5]:


#%matplotlib inline
fig2, ax = plt.subplots(figsize=(5, 3))
ax.scatter(x=data['CDP_TotalEmissions'], 
            y=data['CDP_pct_change2'], 
            marker='o', c='r', edgecolor='b')
ax.set_title('Scatter: TotalEmissions versus pct_change')
ax.set_xlabel('TotalEmissions')
ax.set_ylabel('pct_change')
ax.set_xlim(xmin=0, xmax=10000000)
ax.set_ylim(ymin=-0.5, ymax=0.5)

for i, txt in enumerate(data['City']):
    ax.annotate(txt, (data['CDP_TotalEmissions'][i], data['CDP_pct_change2'][i]))


# ### Creation of response variable

# In[6]:


data['Emission_Population'] = data['CDP_TotalEmissions']/data['CDP_Population']


# In[7]:


#%matplotlib inline
fig2, ax = plt.subplots(figsize=(5, 3))
ax.scatter(x=data['Emission_Population'], 
            y=data['CDP_pct_change2'], 
            marker='o', c='r', edgecolor='b')
ax.set_title('Scatter: TotalEmissions/Pop versus pct_change')
ax.set_xlabel('Emission / Population')
ax.set_ylabel('pct_change')
ax.set_xlim(xmin=0, xmax=60)
ax.set_ylim(ymin=-0.5, ymax=0.5)

for i, txt in enumerate(data['City']):
    ax.annotate(txt, (data['Emission_Population'][i], data['CDP_pct_change2'][i]))


#  
# 1. Binary classification  
# 
# Cities with a percentage change greater than 0 (reduction in emissions) or a number of emissions/population < 5

# In[8]:


data['Classif'] = np.where((data['Emission_Population'] < 5) | 
                                   (data['CDP_pct_change2'] < 0), 0, 1)
data['Classif'].value_counts()


# In[9]:


#%matplotlib inline
fig3, ax = plt.subplots(figsize=(5, 3))
ax.scatter(x=data['Emission_Population'], 
            y=data['CDP_pct_change2'], 
            marker='o', c=data['Classif'], edgecolor='b')
ax.set_title('Scatter: Emission_Population versus pct_change')
ax.set_xlabel('Emission_Population')
ax.set_ylabel('pct_change')
ax.set_xlim(xmin=0, xmax=60)
ax.set_ylim(ymin=-0.5, ymax=0.5)


# ### Drop columns with missing values

# In[10]:


missings = data.isna().sum()/len(data)
missings = missings.reset_index(name="n")

missings[missings['n'] < 0.5]


# In[11]:


data.to_csv('../data/02_output/02_DataToModel.csv')


# ## Data by year city

# In[12]:


data2 = pd.read_csv('../data/02_output/01_DataToPreProcYear.csv', sep=',', index_col = ['Unnamed: 0'])
data2['City'] = data2['City'].str.strip()
print(data2.shape,data2.columns.values)
#data


# ### Detection of outliers

# In[13]:


#%matplotlib inline
fig2, ax = plt.subplots(figsize=(5, 3))
ax.scatter(x=data2['CDP_TotalEmissions'], 
            y=data2['CDP_pct_change2'], 
            marker='o', c='r', edgecolor='b')
ax.set_title('Scatter: TotalEmissions versus pct_change')
ax.set_xlabel('TotalEmissions')
ax.set_ylabel('pct_change')
ax.set_xlim(xmin=0, xmax=10000000)
ax.set_ylim(ymin=-0.5, ymax=0.5)

#for i, txt in enumerate(data2['City']):
#    ax.annotate(txt, (data2['CDP_TotalEmissions'][i], data2['CDP_pct_change2'][i]))


# ### Creation of response variable

# In[14]:


data2['Emission_Population'] = data2['CDP_TotalEmissions']/data2['CDP_Population']


# In[15]:


#%matplotlib inline
fig2, ax = plt.subplots(figsize=(5, 3))
ax.scatter(x=data2['Emission_Population'], 
            y=data2['CDP_pct_change2'], 
            marker='o', c='r', edgecolor='b')
ax.set_title('Scatter: TotalEmissions/Pop versus pct_change')
ax.set_xlabel('Emission / Population')
ax.set_ylabel('pct_change')
ax.set_xlim(xmin=0, xmax=60)
ax.set_ylim(ymin=-0.5, ymax=0.5)

#for i, txt in enumerate(data2['City']):
#    ax.annotate(txt, (data2['Emission_Population'][i], data2['CDP_pct_change2'][i]))


#  
# 1. Binary classification  
# 
# Cities with a percentage change greater than 0 (reduction in emissions) or a number of emissions/population < 1.  
# 
# Group 1 corresponds to cities that are going in the right direction into reducing gas emissions.  
# Group 2 corresponds to cities with no change. 
# Group 3 corresponds to cities with increment or no information  

# In[19]:


data2['Classif2'] = np.where((data2['Emission_Population'] < 0.5) | 
                                   (data2['CDP_pct_change2'] < 0) | 
                            (data2['CDP_Reduction2'] == 'Decreased'), 1, 0)

data2['Classif3'] = np.where((data2['Emission_Population'] < 0.5) | 
                                   (data2['CDP_pct_change2'] < 0) | 
                            (data2['CDP_Reduction2'] == 'Decreased'), 1, 
                             np.where((data2['CDP_pct_change2'] == 0) | 
                            (data2['CDP_Reduction2'] == 'No change'), 2, 3))
data2['Classif2'].value_counts()


# In[20]:


#%matplotlib inline
fig3, ax = plt.subplots(figsize=(5, 3))
scatter = ax.scatter(x=data2['Emission_Population'], 
            y=data2['CDP_pct_change2'], 
            marker='o', c=data2['Classif2'], edgecolor='b')
ax.set_title('Scatter: Emission versus pct_change')
ax.set_xlabel('CDP_TotalEmissions')
ax.set_ylabel('pct_change')
ax.set_xlim(xmin=0, xmax=60)
ax.set_ylim(ymin=-0.5, ymax=0.5)

legend1 = ax.legend(*scatter.legend_elements(),
                    loc="upper right", title="Classes")
ax.add_artist(legend1)


# In[18]:


data2.to_csv('../data/02_output/02_DataToModelYear.csv')


# In[ ]:





# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Unsupervised-classification" data-toc-modified-id="Unsupervised-classification-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Unsupervised classification</a></span><ul class="toc-item"><li><span><a href="#Standardize-dataset" data-toc-modified-id="Standardize-dataset-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Standardize dataset</a></span></li><li><span><a href="#Impute-missing-values" data-toc-modified-id="Impute-missing-values-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Impute missing values</a></span></li><li><span><a href="#Kmeans-classification" data-toc-modified-id="Kmeans-classification-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Kmeans classification</a></span><ul class="toc-item"><li><span><a href="#Silhouette" data-toc-modified-id="Silhouette-1.3.1"><span class="toc-item-num">1.3.1&nbsp;&nbsp;</span>Silhouette</a></span></li></ul></li></ul></li><li><span><a href="#Supervised-classification" data-toc-modified-id="Supervised-classification-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Supervised classification</a></span><ul class="toc-item"><li><span><a href="#Standardize-dataset" data-toc-modified-id="Standardize-dataset-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Standardize dataset</a></span></li><li><span><a href="#Impute-missing-values" data-toc-modified-id="Impute-missing-values-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>Impute missing values</a></span></li><li><span><a href="#Split-Data-for-train-and-test-the-model" data-toc-modified-id="Split-Data-for-train-and-test-the-model-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>Split Data for train and test the model</a></span></li><li><span><a href="#Random-forest" data-toc-modified-id="Random-forest-2.4"><span class="toc-item-num">2.4&nbsp;&nbsp;</span>Random forest</a></span><ul class="toc-item"><li><span><a href="#Binary-classification" data-toc-modified-id="Binary-classification-2.4.1"><span class="toc-item-num">2.4.1&nbsp;&nbsp;</span>Binary classification</a></span></li></ul></li></ul></li></ul></div>

# In[1]:


import sklearn as sk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


from sklearn.preprocessing import StandardScaler

#simple imputation
from sklearn.impute import SimpleImputer

#multiple imputation
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

#knn imputation
from sklearn.impute import KNNImputer


# In[3]:


pd.set_option('display.float_format', lambda x: '%.3f' % x)


# In[4]:


data = pd.read_csv('../data/02_output/02_DatatoModelYear.csv', sep=',', index_col = ['Unnamed: 0'])
print(data.shape,data.columns)


# Selection of variables for analysis

# In[5]:


from pandas.core.common import flatten

strings = ['Country Code', 'Country Name', 'City','CDP_Region', 'CDP_Municipality', 'CDP_id',
          'CDP_Reduction2', 'Year']
owid = data.columns[data.columns.str.contains("OWID")]
cdp = data.columns[data.columns.str.contains("CDP")]

gas = data.columns[data.columns.str.contains("Gas")]

cdpNE = cdp[~cdp.isin(['CDP_Date_measure', 'CDP_Latitude', 'CDP_Longitude','CDP_Region', 'CDP_Municipality', 'CDP_id',
       'CDP_Altitude', 'CDP_GDP', 'CDP_Land_Area', 'CDP_Population', 'CDP_Temperature','CDP_Reduction2', 'CDP_inconsistent'])]

calc = ['Emission_Population', 'Classif2', 'Classif3', 'CDP_inconsistent', 'CDP_pct_change2']

ColsForReduction = list(flatten([cdpNE]))
ColsForPrediction =  list(flatten(data.columns[~ data.columns.isin(list(flatten([strings, owid, 
                                    cdpNE, 'Emission_Population', 'Classif2', 'Classif3'])))]))


# Two datasets are created, data for classification using Kmeans and data for model predictions

# In[6]:


data_model = data[ColsForPrediction]

data_classif = data[ColsForReduction]

print(data_model.columns, data_classif.columns)


# ## Unsupervised classification

# In[7]:


dataClassif_toImpute = data_classif#.loc[:, 'CDP_Latitude':'CDP_pct_change2'].values
Response = data.loc[:, ['Classif2']]


# ### Standardize dataset

# In[8]:


sc = StandardScaler()
dataClassif_stand = sc.fit_transform(dataClassif_toImpute)
dataClassif_stand


# ### Impute missing values

# In[9]:


from sklearn.impute import SimpleImputer
mean_imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
mean_imputer = mean_imputer.fit(dataClassif_stand)
dataClassif_imput = mean_imputer.transform(dataClassif_stand)

dataClassif_imput


# In[10]:


np.where(np.isnan(dataClassif_imput))


# ### Kmeans classification

# In[11]:


# find the appropriate cluster number
plt.figure(figsize=(5, 4))
from sklearn.cluster import KMeans
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
    kmeans.fit(dataClassif_imput)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()


# In[12]:


#identify number of clusters
n_clusters = 2


# In[13]:


from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.decomposition import PCA
preprocessor = Pipeline(
       [("scaler", MinMaxScaler()),
        #("pca", PCA(n_components=2, random_state=42))
       ])


# In[14]:


clusterer = Pipeline(
      [
           (
              "kmeans",
              KMeans(
                  n_clusters=n_clusters,
                  init="k-means++",
                  n_init=50,
                  max_iter=500,
                  random_state=42,
            ),
        ),
    ]
 )


# In[15]:


pipe = Pipeline(
        [("preprocessor", preprocessor),
         ("clusterer", clusterer)])


# In[16]:


pipe.fit(dataClassif_imput)


# The Silhouette Coefficient is calculated using the mean intra-cluster distance (a) and the mean nearest-cluster distance (b) for each sample. The Silhouette Coefficient for a sample is (b - a) / max(a, b). To clarify, b is the distance between a sample and the nearest cluster that the sample is not a part of. Note that Silhouette Coefficient is only defined if number of labels is 2 <= n_labels <= n_samples - 1.
# 
# This function returns the mean Silhouette Coefficient over all samples. To obtain the values for each sample, use silhouette_samples.
# 
# The best value is 1 and the worst value is -1. Values near 0 indicate overlapping clusters. Negative values generally indicate that a sample has been assigned to the wrong cluster, as a different cluster is more similar.

# In[17]:


from sklearn.metrics import silhouette_score, adjusted_rand_score
preprocessed_data = pipe["preprocessor"].transform(dataClassif_imput)

predicted_labels = pipe["clusterer"]["kmeans"].labels_

silhouette_score(preprocessed_data, predicted_labels)


# #### Silhouette

# In[18]:


import seaborn as sns

pcadf = pd.DataFrame(
   data_classif[['CDP_TotalEmissions','CDP_pct_change2']]
   )
pcadf["predicted_cluster"] = pipe["clusterer"]["kmeans"].labels_
#pcadf["true_label"] = label_encoder.inverse_transform(true_labels)

plt.style.use("fivethirtyeight")
plt.figure(figsize=(8, 8))
scat = sns.scatterplot(
     "CDP_TotalEmissions",
     "CDP_pct_change2",
     s=50,
     data=pcadf,
     hue="predicted_cluster",
#     style="true_label",
     palette="Set2",
)

scat.set_title(
    "Clustering results from Greenhouse gas emissions data"
 )
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
plt.show()


# In[19]:


#original data with clusters
Clusters_df = pd.DataFrame(data)
Clusters_df.columns = data.columns
Clusters_df["cluster"] = pipe["clusterer"]["kmeans"].labels_
Clusters_df["cluster"].value_counts()


# ## Supervised classification

# In[20]:


dataModel_toImpute = data_model
Response = Clusters_df.loc[:, ['cluster']]#cluster


# ### Standardize dataset

# In[21]:


sc = StandardScaler()
datamodel_stand = sc.fit_transform(dataModel_toImpute)
datamodel_stand


# ### Impute missing values

# In[22]:


imputer = KNNImputer(n_neighbors=2, weights="uniform")
datamodel_imput = imputer.fit_transform(datamodel_stand)
datamodel_imput


# In[23]:


#from sklearn.impute import SimpleImputer
#mean_imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
#mean_imputer = mean_imputer.fit(datamodel_stand)
#datamodel_imput = mean_imputer.transform(datamodel_stand)

#datamodel_imput


# In[24]:


np.where(np.isnan(datamodel_imput))


# In[25]:


X = datamodel_imput
y = Response
print(X.shape, y.shape)


# ### Split Data for train and test the model

# In[26]:


from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split


# 33% of the data is selected for test the model, random_state = 1 allows reproducibility in the selection

# In[27]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
#X_train
#y_train


# ### Random forest

# #### Binary classification

# In[28]:


y1_train = y_train.iloc[:,0]
y1_test = y_test.iloc[:,0]
y1_train


# - n_estimators: The number of trees in the forest.
# - max_depth: The maximum depth of the tree. If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples.  
# - random_state: Controls both the randomness of the bootstrapping of the samples used when building trees (if bootstrap=True) and the sampling of the features to consider when looking for the best split at each node (if max_features < n_features). See Glossary for details.

# In[29]:


from sklearn.ensemble import RandomForestClassifier
model1 = RandomForestClassifier(random_state=0, n_estimators=100, max_depth=4)
model1.fit(X_train, y1_train)


# In[30]:


feature_imp = pd.Series(model1.feature_importances_,index=data_model.columns).sort_values(ascending=False)
feature_imp


# In[31]:


from sklearn import metrics
# make predictions
yhat1 = model1.predict(X_test)
# evaluate predictions
mae1 = metrics.mean_absolute_error(y1_test, yhat1)
print('MAE1: %.3f' % mae1)


# In[32]:


round(model1.score(X_train, y1_train), 4)


# In[33]:


round(model1.score(X_test, y1_test), 4)


# In[34]:


print(metrics.confusion_matrix(y1_test, yhat1))
print(metrics.classification_report(y1_test, yhat1))
print(metrics.accuracy_score(y1_test, yhat1))


# In[35]:


estimator = model1.estimators_[5]

from sklearn.tree import export_graphviz
# Export as dot file
export_graphviz(estimator, out_file='tree1.dot', 
                feature_names = data_model.columns,
                #class_names = data_reduced.target_names,
                rounded = True, proportion = False, 
                precision = 2, filled = True)

# Convert to png using system command (requires Graphviz)
from subprocess import call
call(['dot', '-Tpng', 'tree1.dot', '-o', 'tree1.png', '-Gdpi=600'])

# Display in jupyter notebook
from IPython.display import Image
Image(filename = 'tree1.png')


# In[36]:


#original data with predictions
Clusters_df["predictions"] = model1.predict(X)
Clusters_df.shape


# In[37]:


#save csv with clusters
Clusters_df.to_csv('../data/02_output/03_Clusters.csv')


# In[ ]:





# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Create-Map" data-toc-modified-id="Create-Map-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Create Map</a></span></li></ul></div>

# In[1]:


import plotly.express as px
import pandas as pd


# In[2]:


df = pd.read_csv('../data/02_output/03_Clusters.csv', sep=',', index_col = ['Unnamed: 0'])
df[['City','Year','CDP_TotalEmissions','CDP_pct_change2', 'Classif2','cluster','predictions']]


# In[3]:


print(str(df['Country Name'].nunique()) + " Countries and " +
str(df.City.nunique()) + ' Cities, data from ' + str(df.Year.min()) + " to " + str(df.Year.max()) + ".")


# Total Emissions based on tree absorbtion
# https://www.viessmann.co.uk/heating-advice/how-much-co2-does-tree-absorb

# In[4]:


df['TreeHelp'] = (df['CDP_TotalEmissions']/1000)/21


# In[5]:


coordinates = df.groupby(['Country Code','Country Name'])['CDP_Latitude','CDP_Longitude'].mean().reset_index()
#coordinates
#coordinates.to_csv('coordinates.csv')


# In[7]:



#Countries with bad behaviour
print(df[df.predictions ==1]['Country Code'].nunique(),

#Cities with good behaviour
df[df.predictions ==0]['Country Code'].nunique())

#Cities with bad behaviour
print(df[df.predictions ==1]['City'].nunique(),

#Cities with good behaviour
df[df.predictions ==0]['City'].nunique())

#Total Emissions in cities with bad behaviour
print(df[df.predictions ==1]['CDP_TotalEmissions'].sum().round(1),

#Total Emissions in cities with good behaviour
df[df.predictions ==0]['CDP_TotalEmissions'].sum().round(1))

#Percentage change in cities with bad behaviour
print(round(df[df.predictions ==1]['CDP_pct_change2'].mean(),3),

#Percentage change in cities with good behaviour
round(df[df.predictions ==0]['CDP_pct_change2'].mean(),3))


# In[11]:


df['PredictedGroup'] = np.where(df['predictions'] == 1, 'Good', 'Bad')

df['PredictedGroup'].value_counts()


# ### Create Map

# In[8]:


mapdf = df.sort_values(by=['Year'])
#customdata  = np.stack((mapdf['City'], mapdf['Year'],mapdf['CDP_TotalEmissions'], mapdf['CDP_pct_change2']), axis=-1)
customdata  = mapdf[['City','Year','CDP_TotalEmissions','CDP_pct_change2']]

#mapdf = df
#Create map figure 
fig1 = px.scatter_geo(
    mapdf, #emissions data
    lat = mapdf['CDP_Latitude'], #latitude data
    lon = mapdf['CDP_Longitude'], #longitude data
    #zoom = 0.5, #Starting zoom level
    color = 'predictions', #Colored by Emissions per capita  
    color_continuous_scale=[(0.00, "green"), (0.2, "green"),
                            (0.4, "green"), (0.6, "red"),
                            (0.8, "red"),  (1.00, "red")],#'RdYlGn_r', #Color scale for Emissions per capita
    size = 'CDP_TotalEmissions', #size of markers based on Emissions
    size_max = 50, #Create scale for marker sizes
    opacity = .6,
    range_color = (0,1),
    animation_frame = 'Year', 
    hover_name = 'City',
    hover_data = {'City':False, 'CDP_Latitude':False,'CDP_Longitude':False,'predictions':False, 
                  'CDP_TotalEmissions':False, 'CDP_pct_change2':False}, #data to be displayed when mouse is hovered over point
     #mapbox_style="carto-positron", #for flat map
    projection = 'natural earth'
)
fig1.update_layout(coloraxis_colorbar=dict(
    title="Clasification",
    tickvals=[0.2,0.8],
    ticktext=["Bad behaviour", "Good behaviour"],
    lenmode="pixels", len=100
))
fig1.update_traces(
    hovertemplate='<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Total Emissions: %{customdata[2]:.0f} <br>Percentage change: %{customdata[3]:.2%}'
    #hovertemplate='<b>%{customdata[0]}</b>%{customdata[1]}'
)


# In[ ]:


customdata


# Filter data by country to perform this bar chart

# In[ ]:


barchart = px.bar(
        data_frame=df,
        x=df['Year'],
        y=df['CDP_TotalEmissions'],
        #title=y_axis + ': by ' + x_axis,
        color=df['City'],
        # facet_col='Borough',
        # color='Borough',
        barmode='stack',
        
    )

barchart.update_layout(xaxis={'categoryorder': 'total ascending'},
                           title={'xanchor': 'center', 
                                  'yanchor': 'top', 
                                  'y': 0.9, 
                                  'x': 0.5, })


# In[ ]:




