import json
from collections import defaultdict
import matplotlib.pyplot as plt

with open('test2.json', 'r') as file:
    data = json.load(file)

sumy_energii = defaultdict(float)
liczniki_godzin = defaultdict(int)

for wpis in data.values():
    godzina = int(wpis["Godzina"])
    energia_str = wpis["Zrodla_fotowoltaiczne"].replace(",", ".")
    energia = float(energia_str)
    
    sumy_energii[godzina] += energia
    liczniki_godzin[godzina] += 1

godziny = range(1, 25)  
srednie_energii = []
for godzina in godziny:
    if godzina in sumy_energii and liczniki_godzin[godzina] > 0:
        srednia = sumy_energii[godzina] / liczniki_godzin[godzina]
    else:
        srednia = 0.0
    srednie_energii.append(srednia)


print("Średnia produkcja energii słonecznej w kwietniu [MWh]:")
for godzina, srednia in zip(godziny, srednie_energii):
    print(f"Godzina {godzina:2d}: {srednia:.2f} MWh")


plt.figure(figsize=(12, 6))
plt.bar(godziny, srednie_energii, color='orange', edgecolor='black')
plt.title("Średnia produkcja energii słonecznej w kwietniu")
plt.xlabel("Godzina")
plt.ylabel("Średnia produkcja [MWh]")
plt.xticks(godziny)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()