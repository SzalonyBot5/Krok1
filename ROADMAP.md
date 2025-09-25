📌 Roadmapa trenowania modeli (LightGBM, MLP, LSTM) – w logicznej kolejności

1. Dane wejściowe

1.  Pobranie danych
    -   z Binance REST API (historyczne OHLCV),
    -   z Binance WebSocket (dane RT – do testowania modelu).
2.  Wstępne przetwarzanie
    -   sprawdzenie braków (NaN), uzupełnienie (ffill, bfill,
        interpolacja),
    -   usunięcie duplikatów,
    -   wyrównanie interwałów (np. 1m, 5m, 1h).
3.  Inżynieria cech
    -   wskaźniki techniczne (RSI, MACD, EMA, Bollinger Bands),
    -   wolumeny, zmienność, zwroty logarytmiczne.
4.  Podział zbioru
    -   dane treningowe (70%),
    -   walidacyjne (15%),
    -   testowe (15%) – zawsze w kolejności czasowej.
5.  Skalowanie
    -   LightGBM – nie wymaga, opcjonalnie normalizacja cech,
    -   MLP – StandardScaler (średnia 0, wariancja 1),
    -   LSTM – MinMaxScaler (0–1).

2. Budowa modelu

LightGBM

-   Dane: tablica (X, y).
-   Hiperparametry:
    1.  objective,
    2.  num_leaves, max_depth,
    3.  learning_rate,
    4.  n_estimators,
    5.  feature_fraction, bagging_fraction.

MLP (Multi-Layer Perceptron)

-   Dane: znormalizowane wektory.
-   Architektura:
    1.  Input layer (liczba cech),
    2.  Hidden layers (ReLU),
    3.  Dropout,
    4.  Output layer.

LSTM

-   Dane: sekwencje (samples, timesteps, features).
-   Architektura:
    1.  Okno czasowe,
    2.  Warstwa LSTM,
    3.  Dropout,
    4.  Dense(1).

3. Trenowanie modeli

-   fit() na train,
-   walidacja na val,
-   unikanie overfittingu: Dropout, regularyzacja, EarlyStopping.

4. Ocena jakości

-   Regresja: MAE, RMSE, R2,
-   Klasyfikacja: accuracy, precision, recall, f1, ROC AUC.

5. Zapisywanie modeli

-   LightGBM: model.save_model(“lightgbm_model.txt”),
-   MLP/LSTM: model.save(“mlp_model.keras”).

6. Predykcja

-   Takie samo przetwarzanie danych,
-   model.predict(X_test),
-   interpretacja wyników.

7. Wizualizacja wyników

-   wykres rzeczywiste vs przewidziane,
-   overlay na świecach (mplfinance),
-   macierz pomyłek, loss curve, feature importance.

8. Użycie w czasie rzeczywistym

1.  Zbieranie danych RT z Binance WebSocket,
2.  Aktualizacja okna danych,
3.  Predykcja,
4.  Wizualizacja sygnałów BUY/SELL.

