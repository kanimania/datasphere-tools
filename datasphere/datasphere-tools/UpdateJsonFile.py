import json
import pandas as pd
import re

# Pfade zu den Dateien
excel_file = r"C:\Users\demlotter\OneDrive - Brenntag\Datasphere\CLI Development\Python Workspace\datasphere\datasphere-tools\Local Tests\Source Data.xlsx"  # Excel-Datei
json_file  = r"C:\Users\demlotter\OneDrive - Brenntag\Datasphere\CLI Development\Python Workspace\datasphere\datasphere-tools\Local Tests\Target Data.json"   # JSON-Datei

# Excel-Datei einlesen (angenommen, sie hat Spalten "key" und "value")
df = pd.read_excel(excel_file)

# JSON-Datei einlesen
with open(json_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# print("Original Json: " + str(json_data))

def search_json(data, pattern, parent_key=""):
    # Wenn data ein Dictionary ist
    if isinstance(data, dict):
        for key, value in data.items():
            # Erstelle den vollständigen Schlüsselpfad
            full_key = f"{parent_key}.{key}" if parent_key else key
            
            # Prüfen, ob der aktuelle Schlüssel zur Wildcard passt
            if re.search(pattern, full_key):  # `re.search` sucht nach Übereinstimmungen überall im String
                yield full_key, value  # Wenn der Schlüssel übereinstimmt, gebe ihn und den Wert zurück

            # Rekursiver Aufruf, falls der Wert ein Dictionary oder eine Liste ist
            if isinstance(value, (dict, list)):
                yield from search_json(value, pattern, full_key)  # Übergib den aktuellen Schlüssel als Elternpfad
    
    # Wenn data eine Liste ist, iteriere durch die Liste
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            # Erstelle einen neuen Schlüsselpfad für Listen, indem der Index hinzugefügt wird
            full_key = f"{parent_key}[{idx}]"
            yield from search_json(item, pattern, full_key)

# Hilfsfunktion zum Update von verschachtelten JSON-Daten
def update_json(data, key, value):
    # Temporäre Ersetzung des @EndUserText.label mit einem Platzhalter
    temp_key = key.replace('@EndUserText.label', '@EndUserText_label')  
    # Splitte den Schlüssel nach Punkten, aber ignoriere @EndUserText_label
    keys = temp_key.split('.')  
    # Stelle sicher, dass wir den Platzhalter wieder in @EndUserText.label umwandeln
    keys = [key.replace('@EndUserText_label', '@EndUserText.label') for key in keys]
    print("Keys after split: " + str(keys))
    print("Value to update :" + str(value))
    
    for k in keys[:-1]:
        # Wenn der Wert ein Dictionary ist
        if isinstance(data, dict):
            if k not in data:
                raise KeyError(f"Schlüssel '{k}' fehlt in den Daten")
            # print(f"Verarbeite: {data} -> {k}")
            data = data[k]  # Gehe weiter in die verschachtelte Struktur
        # Wenn der Wert eine Liste ist
        elif isinstance(data, list):
            try:
                index = int(k)  # Versuche, den Schlüssel als Index zu interpretieren
                data = data[index]  # Gehe zur Liste an der angegebenen Position
            except (ValueError, IndexError):
                raise KeyError(f"Der Index '{k}' ist ungültig für die Liste")
        else:
            raise TypeError(f"Erwartet ein Dictionary oder eine Liste, aber {type(data)} wurde gefunden bei Schlüssel '{k}'")

    # Setze den Wert des letzten Schlüssels
    if isinstance(data, dict):
        data[keys[-1]] = value
    else:
        raise TypeError(f"Erwartet ein Dictionary am Ende, aber {type(data)} wurde gefunden bei Schlüssel '{keys[-1]}'")

# Iteriere durch die Excel-Daten und aktualisiere die JSON-Daten
for index, row in df.iterrows():
    key = row['key']  # 'key' ist der Name der Spalte mit den Schlüsseln
    value = row['value']  # 'value' ist der Name der Spalte mit den Werten

    # Entferne etwaige Escape-Zeichen oder Anführungszeichen
    value = value.strip('"')  # Entfernt führende und abschließende Anführungszeichen

    # Beispiel-Wildcard-Suche nach `@EndUserText.label`
    # pattern = r"@EndUserText\.label"  # Sucht nach allen Vorkommen von @EndUserText.label
    # pattern = r"elements\..*\.@EndUserText\.label"
    pattern = r"Any\.@EndUserText\.label"
    dynamic_pattern = pattern.replace("Any", key)
    print("Search Pattern   : " + dynamic_pattern)
    matches = search_json(json_data, dynamic_pattern)
    print("Excel Key        : " + key)
    print("Excel Value      : " + value)
    for keys, values in matches:
        print(f"Gefunden    : {keys} -> {values}")
        update_json(json_data, keys, value)

# Speichern der aktualisierten JSON-Datei
with open(json_file, 'w', encoding='utf-8') as f:
     json.dump(json_data, f, ensure_ascii=False, indent=4)

print("JSON-Datei wurde erfolgreich aktualisiert!")

# Upload JSON Test File Befehl:
# datasphere objects local-tables update --space INGESTION_001 --technical-name TEST_CLI --file-path "C:\Users\demlotter\OneDrive - Brenntag\Datasphere\CLI Development\Python Files\Target JSON.json"