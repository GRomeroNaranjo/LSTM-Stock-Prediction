import torch
import matplotlib.pyplot as plt
import predictor as main


def test_accuracy_individual(ticker, start_date, end_date, test_date, epochs):
    data_train = main.get_stock_data(ticker, start_date, end_date)   
    data_test = main.get_stock_data(ticker, end_date, "2024-08-23")

    run_system = main.RunSystem(n_neurons_1=90, n_neurons_2=60, n_neurons_3=30, n_neurons_4=1)
    run_system.train(data_train, num=90, epochs=epochs)

    X_test, y_test = run_system.preprocess(data_test, num=90)
    run_system.test_accuracy_graph(X_test, y_test)

    predictions, inputs = run_system.predict_trend(data_test, 90, 5)

    plt.plot(inputs + predictions)
    plt.title("Stock Prediction")
    plt.show()

    print(predictions)


test_accuracy_individual("BTC-USD", "2020-01-01", "2023-01-01", "2024-08-31", 1500)
