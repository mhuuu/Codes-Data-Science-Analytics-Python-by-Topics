## 4. Reading in the Data ##

import pandas as pd
data_files = [
    "ap_2010.csv",
    "class_size.csv",
    "demographics.csv",
    "graduation.csv",
    "hs_directory.csv",
    "sat_results.csv"
]
data = {}
data['ap_2010']=pd.read_csv('schools/ap_2010.csv')
data['class_size']=pd.read_csv('schools/class_size.csv')
data['demographics']=pd.read_csv('schools/demographics.csv')
data['graduation']=pd.read_csv('schools/graduation.csv')
data['hs_directory']=pd.read_csv('schools/hs_directory.csv')
data['sat_results']=pd.read_csv('schools/sat_results.csv')



## 5. Exploring the SAT Data ##

data['sat_results'].head()

## 6. Exploring the Remaining Data ##

for key in data:
    print(data[key].head())

## 8. Reading in the Survey Data ##

all_survey=pd.read_csv('schools/survey_all.txt',delimiter='\t',encoding='windows-1252')
d75_survey=pd.read_csv('schools/survey_d75.txt',delimiter='\t',encoding='windows-1252')
survey=pd.concat([all_survey,d75_survey],axis=0)
survey.head()

## 9. Cleaning Up the Surveys ##

survey["DBN"] = survey["dbn"]
survey=survey.loc[:,["DBN", "rr_s", "rr_t", "rr_p", "N_s", "N_t", "N_p", "saf_p_11", "com_p_11", "eng_p_11", "aca_p_11", "saf_t_11", "com_t_11", "eng_t_11", "aca_t_11", "saf_s_11", "com_s_11", "eng_s_11", "aca_s_11", "saf_tot_11", "com_tot_11", "eng_tot_11", "aca_tot_11"]]
data['survey']=survey

## 11. Inserting DBN Fields ##

data['hs_directory']['DBN']=data['hs_directory']['dbn']

def pad_csd(num):
    string_representation = str(num)
    if len(string_representation) > 1:
        return string_representation
    else:
        return string_representation.zfill(2)
data["class_size"]["padded_csd"] = data["class_size"]["CSD"].apply(pad_csd)
data["class_size"]["DBN"] = data["class_size"]["padded_csd"] + data["class_size"]["SCHOOL CODE"]
print(data["class_size"].head())

## 12. Combining the SAT Scores ##

cols = ['SAT Math Avg. Score', 'SAT Critical Reading Avg. Score', 'SAT Writing Avg. Score']
for c in cols:
    data["sat_results"][c] = pd.to_numeric(data["sat_results"][c], errors="coerce")

data['sat_results']['sat_score'] = data['sat_results'][cols[0]] + data['sat_results'][cols[1]] + data['sat_results'][cols[2]]
print(data['sat_results']['sat_score'].head())

## 13. Parsing Geographic Coordinates for Schools ##

import re
def latitude(x):
    coords=re.findall('\(.+\)',x)
    lat=coords[0].split(',')[0].replace('(','')
    return lat
data['hs_directory']['lat']=data['hs_directory']['Location 1'].apply(latitude)
data['hs_directory'].head()

## 14. Extracting the Longitude ##

import re
def longitude(x):
    coords=re.findall('\(.+\)',x)
    lon=coords[0].split(',')[1].replace(')','')
    return lon
data['hs_directory']['lon']=data['hs_directory']['Location 1'].apply(longitude)
data['hs_directory'].head()
for c in ['lat','lon']:
    data["hs_directory"][c] = pd.to_numeric(data["hs_directory"][c], errors="coerce")
data["hs_directory"].head()    
    