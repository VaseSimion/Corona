import ExtractData as Ed
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN, LSTM
import matplotlib.pyplot as plt
import numpy as np

countries = Ed.get_updated_data()
for country in countries:
    if country.name == "United_States_of_America":
        print(country.name)
        print(country.dates_list)
        print(country.cases_list)
        print(country.moving_average_cases)
        print(country.population)
        informationdf = pd.DataFrame(index=country.dates_list, data=country.moving_average_cases, columns=["Cases"])

#print(informationdf)
test_ratio = 0.05
cutoff_point = (int(len(informationdf) * (1 - test_ratio)))
#print(cutoff_point)
traindf = informationdf.iloc[:cutoff_point]
testdf = informationdf.iloc[cutoff_point:]
#print(traindf)
#print(testdf)

scaler = MinMaxScaler()
scaler.fit(traindf)
scaled_train = scaler.transform(traindf)
scaled_test = scaler.transform(testdf)
print(scaled_train)

length = 30
batch_size = 1

generator = TimeseriesGenerator(data=scaled_train, targets=scaled_train, length=length, batch_size=batch_size)
print(generator[130])

n_features = 1  # because we are looking only at number of cases

model = Sequential()
model.add(LSTM(30, input_shape=(length, n_features)))
model.add(Dense(20))
model.add(Dense(1))
model.compile(optimizer="adam", loss="mse")
model.summary()
model.fit_generator(generator, epochs=50)

losses = pd.DataFrame(model.history.history)
plt.plot(losses)
plt.show()

test_predictions = []
first_eval_batch = scaled_train[-length:]
current_batch = first_eval_batch.reshape((1, length, n_features))

for i in range(30):
    current_pred = model.predict(current_batch)[0]
    test_predictions.append(current_pred)
    current_batch = np.append(current_batch[:, 1:, :], [[current_pred]], axis=1)


true_predictions = scaler.inverse_transform(test_predictions)
#testdf["Predictions"] = true_predictions
#print(testdf)

plt.plot(testdf["Cases"])
plt.plot(true_predictions)
plt.legend(["Cases","Predictions"])
plt.xticks([int(x) for x in np.linspace(0, len(true_predictions)-1, num=10)], rotation=20)
plt.show()
