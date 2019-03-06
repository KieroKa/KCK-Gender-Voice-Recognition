import sys
import numpy as np
import soundfile as sf
import scipy.signal as signal
import warnings


# Przypisanie zmiennej do pliku dzwiękowego podanego z argumentu
voice = sys.argv[1]

try:
    # Ignorowanie ostrzeżeń (łatwiejszy odczyt)
    warnings.filterwarnings('ignore')

    # Odczyt pliku
    data, rate = sf.read(voice)

    # Normalizacja wartość mocy sygnału
    data = data.astype(float) / 2**16
    # Zamiana ze stereo do mono w razie potrzeby
    if not isinstance(data[0], float):
        data = data[:, 0] + data[:, 1]

    # Obliczanie wartości 1/4 do obcięcia
    lenght = len(data)
    cut = int(len(data) / 4)

    # Obcięcie 1/4 danych z początku i końca, żeby wyeliminować zakłócenia
    data = data[cut:(lenght-cut)]

    # Przygotowanie danych do próbkowania (okienkowanie, użycie dyskretnej transformaty Fouriera i wartość bezwzględna)
    processed = data * signal.kaiser(len(data), 5.0)
    processed = abs(np.fft.rfft(processed))

    # Sygnał trzy razy wypróbkowany
    decimate2 = signal.decimate(processed, 2)
    decimate3 = signal.decimate(processed, 3)
    decimate4 = signal.decimate(processed, 4)

    lenght = len(decimate4)

    # Wyliczenie sygnału końcowego poprzez przemnożenie wszystkich wypróbkowanych sygnałów do uzyskania "piku"
    end_signal = processed[:lenght] * decimate2[:lenght] * decimate3[:lenght] * decimate4[:lenght]

    # Odcięcie pierwszych 60 Hz
    move = 60

    # Znalezienie najwyższego piku po przesunięciu i uzyskanie częstotliwości
    # przez podzielenie przez rozdzielczość częstotliwości
    result = (np.argmax(end_signal[move:]) + move) / (len(data) / rate)

    # Jeżeli częstotliwość piku jest większa niż 165 to jest to głos kobiecy.
    answer = 'M'
    if result > 165:
        answer = 'K'

    print(answer)

except:
    print('M')
