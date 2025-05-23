import json
from collections import defaultdict

with open('test2.json', 'r') as file:
    data = json.load(file)


sumy_dzienneW = defaultdict(float)
sumy_dzienneS = defaultdict(float)

for wpis in data.values():
    data = wpis["Data"]
    energiaW = float(wpis["Zrodla_wiatrowe"].replace(",", "."))
    energiaS = float(wpis["Zrodla_fotowoltaiczne"].replace(",", "."))
    sumy_dzienneW[data] += energiaW
    sumy_dzienneS[data] += energiaS

dzien_maxW = max(sumy_dzienneW.items(), key=lambda x: x[1])
dzien_maxS = max(sumy_dzienneS.items(), key=lambda x: x[1])
print(f"Najwięcej energii wiatrowej wyprodukowano {dzien_maxW[0]}: {dzien_maxW[1]:.2f} MWh")
print(f"Najwięcej energii słonecznej wyprodukowano {dzien_maxS[0]}: {dzien_maxS[1]:.2f} MWh")