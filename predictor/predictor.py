import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf

class FeedForwardSystem(nn.Module):
    def __init__(self, n_neurons_1, n_neurons_2, n_neurons_3, n_neurons_4):
        super(FeedForwardSystem, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(n_neurons_1, n_neurons_2),
            nn.ReLU(),
            nn.Linear(n_neurons_2, n_neurons_3),
            nn.ReLU(),
            nn.Linear(n_neurons_3, n_neurons_4)
        )
    
    def forward(self, inputs):
        return self.model(inputs)

class SystemTools:
    def __init__(self, n_neurons_1, n_neurons_2, n_neurons_3, n_neurons_4):
        self.model = FeedForwardSystem(n_neurons_1, n_neurons_2, n_neurons_3, n_neurons_4)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()
        self.scaler_X = MinMaxScaler()
        self.scaler_y = MinMaxScaler()

    def convert_tensor(self, x):
        if isinstance(x, torch.Tensor):
            return x
        return torch.from_numpy(x).float()
    
    def scale_fit(self, inputs, is_y=False):
        if is_y:
            return self.scaler_y.fit_transform(inputs.reshape(-1, 1))
        return self.scaler_X.fit_transform(inputs)
    
    def scaler_inverse(self, inputs, is_y=False):
        if is_y:
            return self.scaler_y.inverse_transform(inputs)
        return self.scaler_X.inverse_transform(inputs)
    
    def predict(self, inputs):
        inputs = self.convert_tensor(inputs)
        inputs = inputs.view(1, -1)

        if inputs.shape[1] != 90:
            if inputs.shape[1] > 90:
                inputs = inputs[:, :90]
            else:
                padding = torch.zeros(1, 90 - inputs.shape[1])
                inputs = torch.cat((inputs, padding), dim=1)

        with torch.no_grad():
            return self.model(inputs)

    def train(self, X_train, y_train, epochs):
        X_train = self.convert_tensor(X_train)
        y_train = self.convert_tensor(y_train)

        for epoch in range(epochs):
            self.optimizer.zero_grad()
            output = self.model(X_train)
            loss = self.criterion(output, y_train)
            loss.backward()
            self.optimizer.step()

            print(f"Epoch {epoch + 1}/{epochs} - Loss: {loss.item():.4f}")

    def plot_accuracy_graph(self, X_test, y_test):
        X_test = self.convert_tensor(X_test)
        y_test = y_test.reshape(-1, 1)

        predictions = self.model(X_test).detach().numpy()
        predictions = self.scaler_inverse(predictions, is_y=True)

        plt.plot(predictions, label='Predictions')
        plt.plot(self.scaler_inverse(y_test, is_y=True), label='True Values')
        plt.title("Test Data Accuracy Graph")
        plt.legend()
        plt.show()

class RunSystem:
    def __init__(self, n_neurons_1, n_neurons_2, n_neurons_3, n_neurons_4):
        self.system = SystemTools(n_neurons_1, n_neurons_2, n_neurons_3, n_neurons_4)
        
    def train(self, data, num, epochs):
        X_train, y_train = self.preprocess(data, num)

        X_train = self.system.scale_fit(X_train)
        y_train = self.system.scale_fit(y_train, is_y=True)

        self.system.train(X_train, y_train, epochs)
        self.X_train, self.y_train = X_train, y_train

    def predict_trend(self, data, num, number_days):
        data = list(data)
        predictions = []
        input_data = data[-num:]

        for _ in range(number_days):
            inputs = np.array(data[-num:]).reshape(1, -1)
            inputs_scaled = self.system.scaler_X.transform(inputs)
            inputs_tensor = self.system.convert_tensor(inputs_scaled)

            prediction = self.system.predict(inputs_tensor).detach().numpy()
            prediction = self.system.scaler_inverse(prediction, is_y=True)
            predictions.append(prediction[0, 0])

            data.append(prediction[0, 0])
            data.pop(0)

        return predictions, input_data

    def predict(self, inputs):
        predictions = self.system.predict(inputs)
        return predictions

    def preprocess(self, data, num):
        X_train, y_train = [], []
        for i in range(len(data) - num):
            X_train.append(data[i: i + num])
            y_train.append(data[i + num])
        return np.array(X_train), np.array(y_train)
    
    def test_accuracy_graph(self, X_test, y_test):
        X_test = self.system.scale_fit(X_test)
        y_test = self.system.scale_fit(y_test, is_y=True)
        self.system.plot_accuracy_graph(X_test, y_test)
    

def get_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data['Close'].values

def predict(ticker, start_date, end_date, epochs):
    data_train = get_stock_data(ticker, start_date, end_date)

    run_system = RunSystem(n_neurons_1=90, n_neurons_2=60, n_neurons_3=30, n_neurons_4=1)
    run_system.train(data_train, num=90, epochs=epochs)

    predictions, inputs = run_system.predict_trend(data_train, num=90, number_days=50)

    plt.plot(inputs + predictions)
    plt.title("Stock Prediction")
    plt.show()

    return predictions

predictions = predict("BTC-USD", "2020-01-01", "2024-08-28", 1500)

print(predictions)
