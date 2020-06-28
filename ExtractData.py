from urllib.request import urlopen
import json

class Country:
    def return_moving_average(self, listofdata, period):
        moving_average_list = []
        for index, element in enumerate(listofdata[:-period+1]):
            moving_average_list.append(sum(listofdata[index:index+period])/period)
        return (period-1)*[0] + moving_average_list

    def __init__(self, name, population, cases_list, dates_list):
        self.name = name
        self.population = population
        self.cases_list = cases_list
        self.moving_average_cases = self.return_moving_average(cases_list, 14)
        self.dates_list = dates_list

def get_updated_data():
    url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/json/"
    response = urlopen(url)
    results = json.loads(response.read().decode("utf-8"))
    print(results["records"][0])

    country = results["records"][0]["countriesAndTerritories"]
    current_cases_list = []
    current_dates_list = []
    countries = []
    current_population = results["records"][0]["popData2019"]

    for dictionary in results["records"]:
        if dictionary["countriesAndTerritories"] == country:
            current_cases_list.append(dictionary["cases"])
            current_dates_list.append(dictionary["dateRep"])
        else:
            current_cases_list.reverse()
            current_dates_list.reverse()
            print(country, str(current_cases_list))
            countries.append(Country(name=country, population=current_population,
                                     cases_list=current_cases_list, dates_list=current_dates_list))
            country = dictionary["countriesAndTerritories"]
            current_cases_list = []
            current_dates_list = []
            current_cases_list.append(dictionary["cases"])
            current_dates_list.append(dictionary["dateRep"])
            current_population = dictionary["popData2019"]
    print("\n\n\n\n\n\n\n\n")
    return countries