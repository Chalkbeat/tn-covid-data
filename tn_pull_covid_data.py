import requests
import pandas as pd

url = "https://districtinformation.tnedu.gov/api/districts"

r = requests.get(url)
json = r.json()
df = pd.DataFrame(json)

# Collect and format school listing data

# General info
id = df["id"]
name = df["name"]
address1 = df["address1"]
address2 = df["address2"]
city = df["city"]
zip = df["zip"]
phone = df["phone"]
website = df["website"]
clp = df["clp"]
latitude = df["latitude"]
longitude = df["longitude"]

# Operating model
districtOperatingModel = pd.DataFrame()

for row in df["districtOperatingModel"]:
  df_row = pd.DataFrame(row, index=[0])
  districtOperatingModel = districtOperatingModel.append(df_row, ignore_index=True)

# Region
region = pd.DataFrame()

for row in df["region"]:
  df_row = pd.DataFrame(row, index=[0])
  region = region.append(df_row, ignore_index=True)

# COVID data
covidData = pd.DataFrame()

for row in df["covidData"]:
  df_row = pd.DataFrame(row, index=[0])
  covidData = covidData.append(df_row, ignore_index=True)

df_formatted = pd.concat([id, name, address1, address2, city, zip, phone, website, clp, latitude, longitude, districtOperatingModel, region, covidData], axis=1)

df_formatted.to_csv("tn_covid_district_data.csv", index=False)


# School data

schools = pd.DataFrame()

for district in df["id"]:
  url = "https://districtinformation.tnedu.gov/api/districts/"+str(district)+"/schools"
  r = requests.get(url)
  json = r.json()
  district_data = pd.DataFrame(json)
  for school in district_data:
    id = district_data["id"]
    districtId = district_data["districtId"]
    name = district_data["name"]
    address1 = district_data["address1"]
    address2 = district_data["address2"]
    city = district_data["city"]
    zip = district_data["zip"]
    phone = district_data["phone"]
    website = district_data["website"]
    canSubmitCovidData = district_data["canSubmitCovidData"]
    latitude = district_data["latitude"]
    longitude = district_data["longitude"]
    # Operating model
    schoolOperatingModel = pd.DataFrame()
    for column in district_data["schoolOperatingModel"]:
      df_row = pd.DataFrame(column, index=[0])
      df_row = df_row.drop(['operatingModel'], axis=1)
      df_subrow = pd.DataFrame.from_dict([column["operatingModel"]])
      df_row = pd.concat([df_row,df_subrow], axis=1)
      df_row.columns = ["schoolOperatingModel_id","schoolOperatingModel_restrictions","schoolOperatingModel_restrictionEndDate",
                        "schoolOperatingModel_lastUpdatedDate","schoolOperatingModel_lastUpdatedBy", "schoolOperatingModel_restrictionReason",
                        "operatingModel_id", "operatingModel_name", "operatingModel_color", "operatingModel_active"]
      schoolOperatingModel = schoolOperatingModel.append(df_row, ignore_index=True)
    # COVID data
    covidDataSchool = pd.DataFrame()
    for column in district_data["covidData"]:
      df_row = pd.DataFrame(column, index=[0])
      covidDataSchool = covidDataSchool.append(df_row, ignore_index=True)
    school = pd.concat([id, districtId, name, address1, address2, city, zip, phone, website, canSubmitCovidData, latitude, longitude, schoolOperatingModel, covidDataSchool], axis=1)
    schools = schools.append(school, ignore_index=True)

schools.to_csv("tn_covid_schools_data.csv", index=False)
