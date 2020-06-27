from urllib.request import urlopen
import json

url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/json/"
response = urlopen(url)
results = json.loads(response.read().decode("utf-8"))
print(results["records"][0])

country = "Afghanistan"
for dictionary in results["records"]:
    if dictionary["countriesAndTerritories"] == country:
        print(dictionary["cases"])
