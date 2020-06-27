from urllib.request import urlopen
import json
import matplotlib.pyplot as plt

url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/json/"
response = urlopen(url)
results = json.loads(response.read().decode("utf-8"))
print(results["records"][0])


class Country:

    def return_moving_average(self, listofdata, period):
        moving_average_list = []
        for index, element in enumerate(listofdata[:-period+1]):
            moving_average_list.append(sum(listofdata[index:index+period])/period)
        return period*[0] + moving_average_list

    def __init__(self, name, population, cases_list):
        self.name = name
        self.population = population
        self.cases_list = cases_list
        self.moving_average_cases = self.return_moving_average(cases_list, 14)

show_just_ma = True

country = results["records"][0]["countriesAndTerritories"]
cases_list = []
countries = []
population = results["records"][0]["popData2019"]

for dictionary in results["records"]:
    if dictionary["countriesAndTerritories"] == country:
        cases_list.append(dictionary["cases"])
    else:
        cases_list.reverse()
        print(country, str(cases_list))
        countries.append(Country(name=country, population=population, cases_list=cases_list))
        country = dictionary["countriesAndTerritories"]
        cases_list = []
        cases_list.append(dictionary["cases"])
        population = dictionary["popData2019"]

print(len(countries))
legend_list = []
for country in countries:
    if country.name in ["Romania", "Denmark", "Italy", "United_States_of_America"]:
        if not show_just_ma:
            plt.plot([1000000*x/country.population for x in country.cases_list])
            legend_list.append(country.name)
        plt.title("Corona 2020")
        plt.plot([1000000*x/country.population for x in country.moving_average_cases])
        legend_list.append(country.name + "-moving average")
plt.ylabel("New cases per million inhabitants")
plt.legend(legend_list)
plt.show()

print(sum(country.cases_list[-14:])/14/country.population)


