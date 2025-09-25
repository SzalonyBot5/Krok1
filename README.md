RODZAJE MODELI


---

1️⃣ LightGBM

Typ: Gradient Boosting (drzewa decyzyjne)

Dane wejściowe: tablicowe, cechy techniczne (OHLCV, średnie ruchome, wskaźniki typu RSI, MACD, Bollinger Bands itp.)

Najlepsze zastosowania:

Regresja: przewidywanie ceny za określony czas (np. 1h, 4h)

Klasyfikacja: wzrost/spadek ceny w następnym kroku


Plusy: szybkie trenowanie na CPU, odporne na szum w danych, nie wymaga skomplikowanego preprocessing’u

Minusy: nie wyłapuje sekwencyjnych zależności czasowych tak dobrze jak LSTM



---

2️⃣ MLP (Multi-Layer Perceptron / Dense Network)

Typ: Sieć neuronowa gęsto połączona

Dane wejściowe: tablicowe cechy techniczne, ewentualnie okna czasowe jako spłaszczone wektory

Najlepsze zastosowania:

Regresja: przewidywanie ceny lub zmiany ceny

Klasyfikacja: wzrost/spadek, sygnały kupna/sprzedaży


Plusy: prosta implementacja, da się trenować na telefonie

Minusy: słaba przy bardzo długich sekwencjach, wymaga normalizacji danych



---

3️⃣ LSTM (Long Short-Term Memory / RNN)

Typ: Rekurencyjna sieć neuronowa

Dane wejściowe: sekwencje czasowe (np. okna 30 ostatnich świeczek OHLCV)

Najlepsze zastosowania:

Regresja czasowa: przewidywanie przyszłych wartości cen

Sekwencyjna klasyfikacja: wzrost/spadek w kolejnej świeczce, sygnały tradingowe







