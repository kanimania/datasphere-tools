from dsp_utils import dspUtils as du

# Files
csv_file = r"datasphere\datasphere-tools\dsp_files\dsp_source_metadata\B25_Export_Metadata_ZDS_AGR_TEXTS.csv"
json_file = r"datasphere\datasphere-tools\Local Tests\Target Data.json"

# Read CSV file
csv_data = du.read_csv_file(csv_file)

# Read JSON file
json_data = du.read_json_file(json_file)

# Iterate through the CSV data and update the JSON data
for index, row in csv_data.iterrows():
    key = row['FIELDNAME']  # 'key' is the name of the column with the keys
    value = row['FIELDTEXT']  # 'value' is the name of the column with the values

    # Remove any escape characters or quotes
    value = value.strip('"')  # Removes leading and trailing quotes

    # Example wildcard search for `@EndUserText.label`
    # pattern = r"@EndUserText\.label"  # Searches for all occurrences of @EndUserText.label
    # pattern = r"elements\..*\.@EndUserText\.label"
    pattern = r"Any\.@EndUserText\.label"
    dynamic_pattern = pattern.replace("Any", key)
    print("Search Pattern   : " + dynamic_pattern)
    matches = du.search_json(json_data, dynamic_pattern)
    print("Csv Key        : " + key)
    print("Csv Value      : " + value)
    for keys, values in matches:
        print(f"Found    : {keys} -> {values}")
        du.update_json(json_data, keys, value)

# Save the updated JSON file
du.write_json_file(json_data, json_file)