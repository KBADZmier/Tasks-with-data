import json
import math
from datetime import datetime

# Stałe
MAX_STORAGE_CAPACITY = 200000.0  
PLIK_PRODUKCJA = 'test2.json'
PLIK_ZAPOTRZEBOWANIE = 'test3.json'

# Funkcja do parsowania stringów liczbowych z przecinkiem jako separatorem dziesiętnym
def parse_energy_value(value_str):
    return float(value_str.replace(',', '.'))


try:
    with open(PLIK_PRODUKCJA, 'r', encoding='utf-8') as f:
        produkcja_raw_data = json.load(f)
except FileNotFoundError:
    print(f"Błąd: Nie znaleziono pliku {PLIK_PRODUKCJA}")
    exit()
except json.JSONDecodeError:
    print(f"Błąd: Niepoprawny format JSON w pliku {PLIK_PRODUKCJA}")
    exit()

try:
    with open(PLIK_ZAPOTRZEBOWANIE, 'r', encoding='utf-8') as f:
        zapotrzebowanie_raw_data = json.load(f)
except FileNotFoundError:
    print(f"Błąd: Nie znaleziono pliku {PLIK_ZAPOTRZEBOWANIE}")
    exit()
except json.JSONDecodeError:
    print(f"Błąd: Niepoprawny format JSON w pliku {PLIK_ZAPOTRZEBOWANIE}")
    exit()

mapa_produkcji = {}
for key, rekord in produkcja_raw_data.items():
    data_str = rekord['Data']
    godzina_int = int(rekord['Godzina'])
    
    produkcja_wiatrowa_str = rekord.get('Zrodla_wiatrowe', "0,0")
    produkcja_pv_str = rekord.get('Zrodla_fotowoltaiczne', "0,0")
    
    produkcja_wiatrowa = parse_energy_value(produkcja_wiatrowa_str)
    produkcja_pv = parse_energy_value(produkcja_pv_str)
    calkowita_produkcja = produkcja_wiatrowa + produkcja_pv
    
    mapa_produkcji[(data_str, godzina_int)] = calkowita_produkcja

# Lista do przechowywania połączonych danych godzinowych dla kwietnia
dane_godzinowe_kwiecien = []
for key, rekord in zapotrzebowanie_raw_data.items():
    data_str = rekord['Data']
    godzina_int = int(rekord['Godzina'])
    

    if not data_str.startswith("2024-04"):
        continue
        
    zapotrzebowanie = parse_energy_value(rekord['Zapotrzebowanie'])
    
  
    produkcja = mapa_produkcji.get((data_str, godzina_int), 0.0)
    if (data_str, godzina_int) not in mapa_produkcji:
        print(f"Ostrzeżenie: Brak danych o produkcji dla {data_str} godz. {godzina_int}. Przyjęto 0 MWh.")

    dane_godzinowe_kwiecien.append({
        'data': data_str,
        'godzina': godzina_int,
        'zapotrzebowanie': zapotrzebowanie,
        'produkcja': produkcja
    })

# Sortowanie danych chronologicznie
dane_godzinowe_kwiecien.sort(key=lambda x: (x['data'], x['godzina']))


aktualny_poziom_magazynu = 0.0 
min_poziom_magazynu_w_symulacji = 0.0

if not dane_godzinowe_kwiecien:
    print("Brak danych dla kwietnia. Nie można przeprowadzić obliczeń.")
else:
    for wpis_godzinowy in dane_godzinowe_kwiecien:
        produkcja = wpis_godzinowy['produkcja']
        zapotrzebowanie = wpis_godzinowy['zapotrzebowanie']
        
        energia_netto = produkcja - zapotrzebowanie
        
        if energia_netto > 0:  # Nadwyżka energii
            aktualny_poziom_magazynu = min(aktualny_poziom_magazynu + energia_netto, MAX_STORAGE_CAPACITY)
        else:  # Deficyt energii (energia_netto jest <= 0)
            aktualny_poziom_magazynu += energia_netto
            
        # Śledzenie minimalnego poziomu
        if aktualny_poziom_magazynu < min_poziom_magazynu_w_symulacji:
            min_poziom_magazynu_w_symulacji = aktualny_poziom_magazynu


wymagany_pocz_poziom = 0.0
if min_poziom_magazynu_w_symulacji < 0:

    wymagany_pocz_poziom = math.ceil(abs(min_poziom_magazynu_w_symulacji))
else:
   
    wymagany_pocz_poziom = 0.0

wynik_koncowy = int(wymagany_pocz_poziom)

# --- Wyświetlenie wyników ---
print(f"Maksymalna pojemność magazynów: {MAX_STORAGE_CAPACITY} MWh")
print(f"Minimalny obliczony poziom energii w magazynie (przy założeniu startu od 0 MWh): {min_poziom_magazynu_w_symulacji:.3f} MWh")
print(f"Najmniej energii, która powinna być zmagazynowana na początku 1 kwietnia (godz. 00:00), aby zaspokoić kwietniowe zapotrzebowanie: {wynik_koncowy} MWh")