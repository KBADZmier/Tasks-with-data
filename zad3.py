import json
from collections import defaultdict

with open('test2.json', 'r') as file:
    data = json.load(file)


entries = []
for date, entries_data in data.items():
    for hour_data in entries_data:
        entries.append((
            date,
            int(hour_data["Godzina"]),
            float(hour_data["Zrodla_wiatrowe"].replace(",", "."))
        ))


entries.sort(key=lambda x: (x[0], x[1]))

max_length = 0
current_length = 1
start_index = 0
best_start = None
best_end = None

for i in range(1, len(entries)):
    if entries[i][2] > entries[i-1][2]:  # Jeśli energia rośnie
        current_length += 1
    else:
        if current_length > max_length:
            max_length = current_length
            best_start = entries[start_index]
            best_end = entries[i-1]
        current_length = 1
        start_index = i

# Sprawdzenie ostatniego przedziału
if current_length > max_length:
    max_length = current_length
    best_start = entries[start_index]
    best_end = entries[-1]

if best_start and best_end:
    print(f"Najdłuższy rosnący przedział:")
    print(f"Początek: {best_start[0]} godz. {best_start[1]}:00")
    print(f"Koniec: {best_end[0]} godz. {best_end[1]}:00")
    print(f"Długość przedziału: {max_length} godzin")
