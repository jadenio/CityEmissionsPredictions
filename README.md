# Predicting Future Global City Emissions Trends
Using publicly available data from cities who report their annual CO2 emissions, this project builds a predictive model for each city's future CO2 emissions. More specifically, the goal is to determine which cities are on track to meet global carbon emissions reduction goals by the year 2030.

This project uses data from: [data.cdp.net](https://data.cdp.net/Emissions/2020-City-Wide-Emissions/p43t-fbkj).  

Folders:  

**code:** include all the steps for data analysis
- **00_CDPEmissions_merge.ipynb** Clean and merge datasets from 2012 to 2020 from CDPE.
- **00_ExternalDataset_merge.ipynd** Clean and merge all external datasets from 2012 to 2020 from different sources.
- **01_DescriptionOfData.ipynb** Merge and save csv file with CDPE and external datasets. 

**data:** include csv files from each code
- **01_input** datasets to clean
- **02_output** cleaned datasets

The project has the following steps:  
1 - Read and description of datasets.  

2 - Data preprocessing.  

3 - Feature engineering.

4 - Building a predictive model for each city's future CO2 emissions.

5 - Obtaining city lat and lon coordinates through Google Map API.

6 - Creating interactive world map which contains historic and predicted future CO2 emissions for each city.

The final product includes an interactive world map, with a sliding scale to see how emissions for each city change over the years:

![Screenshot](https://i.imgur.com/GkHPGuh.png)



