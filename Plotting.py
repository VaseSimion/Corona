import matplotlib.pyplot as plt
import numpy as np
import ExtractData as Ed


show_just_ma = True

countries_to_show = ["Romania", "Denmark", "Italy", "United_States_of_America", "Brazil", "United_Kingdom"]
countries = Ed.get_updated_data()

x_length = 0
legend_list = []
for country in countries:
    if country.name in countries_to_show:
        x_length = max(x_length,len(country.dates_list))
        if not show_just_ma:
            plt.plot(country.dates_list, [1000000*x/country.population for x in country.cases_list])
            legend_list.append(country.name)
        plt.title("Corona 2020")
        plt.plot(country.dates_list, [1000000*x/country.population for x in country.moving_average_cases])
        legend_list.append(country.name + "-moving average")
plt.xticks([int(x) for x in np.linspace(0, x_length-1, num=10)], rotation=20)
plt.ylabel("New cases per million inhabitants")
plt.legend(legend_list)
plt.show()
print([int(x) for x in np.linspace(0, x_length, num=11)])


