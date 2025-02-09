import pandas as pd
import json

# Pfade zu den Dateien
excel_file = r"C:\Users\demlotter\OneDrive - Brenntag\Datasphere\CLI Development\Python Files\Source Metadata.xlsx"  # Excel-Datei
json_file  = r"C:\Users\demlotter\OneDrive - Brenntag\Datasphere\CLI Development\Python Files\Target JSON.json"  # JSON-Datei

# Excel-Datei einlesen (angenommen, sie hat Spalten "key" und "value")
df = pd.read_excel(excel_file)

# JSON-Datei einlesen
with open(json_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

print("Original Json: " + str(json_data))

# Iteriere durch die Excel-Daten und aktualisiere die JSON-Daten
for index, row in df.iterrows():
    key = row['key']  # 'key' ist der Name der Spalte mit den Schlüsseln
    value = row['value']  # 'value' ist der Name der Spalte mit den Werten
    print(key)
    print(value)
    key = '[definitions][TEST_CLI][elements][Column1][@EndUserText.label]'
    if key in json_data:
         json_data[key] = value  # Aktualisiere den Wert im JSON
    else:
        json_data[key] = value  # Falls der Schlüssel noch nicht existiert, füge ihn hinzu

# # Speichern der aktualisierten JSON-Datei
# with open(json_file, 'w', encoding='utf-8') as f:
#     json.dump(json_data, f, ensure_ascii=False, indent=4)

print("JSON-Datei wurde erfolgreich aktualisiert!")
print(json_data)
