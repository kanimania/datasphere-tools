import pandas as pd
from dsp_utils import dspUtils as du

# Files
excel_file = r"datasphere\datasphere-tools\local tests\Source Data.xlsx"
json_file  = r"datasphere\datasphere-tools\local tests\Target Data.json"

# Read Excel file
df = pd.read_excel(excel_file)

# Read JSON file
json_data = du.read_json_file(json_file)

# Iterate through the CSV data and update the JSON data
for index, row in df.iterrows():
    key = row['key']  # 'key' ist der Name der Spalte mit den Schlüsseln
    value = row['value']  # 'value' ist der Name der Spalte mit den Werten

    # Remove any escape characters or quotes
    value = value.strip('"')  # Removes leading and trailing quotes

    # Example wildcard search for `@EndUserText.label`
    # pattern = r"@EndUserText\.label"  # Searches for all occurrences of @EndUserText.label
    # pattern = r"elements\..*\.@EndUserText\.label"
    pattern = r"Any\.@EndUserText\.label"
    dynamic_pattern = pattern.replace("Any", key)
    print("Search Pattern   : " + dynamic_pattern)
    matches = du.search_json(json_data, dynamic_pattern)
    print("Excel Key        : " + key)
    print("Excel Value      : " + value)
    for keys, values in matches:
        print(f"Gefunden    : {keys} -> {values}")
        du.update_json(json_data, keys, value)

# Save the updated JSON file
du.write_json_file(json_data, json_file)