from dsp_utils import dspUtils as du
import json

# File paths
csv_file = r"C:\temp\B25_Export_Metadata_ZDS_AGR_USERS.csv"  # CSV-File
# Convert the DataFrame to a Dictionary
df = du.read_csv_file(csv_file)
data_dict = df

# # Convert the DataFrame to a Dictionary
# csv_dict = csv_data.to_dict(orient='records')
# print(csv_dict[0])

json_template = {
    "definitions": {
        "DUMMY_TABNAME": {
            "kind": "entity",
            "@ObjectModel.modelingPattern": {
                    "#": "DATA_STRUCTURE"
            },
            "@ObjectModel.supportedCapabilities": [
                {
                    "#": "DATA_STRUCTURE"
                }
            ],
            "@EndUserText.label": "DUMMY_TABLE_TEXT",
            "elements": {
                "DUMMY_COLUMN": {
                    "type": "DUMMY_TYPE",
                    "precision": 0,
                    "scale": 0,
                    "@EndUserText.label": "DUMMY_COLUMN_TEXT"
                },
                "AGR_NAME": {
                    "type": "DUMMY_TYPE2",
                    "precision": 0,
                    "scale": 0,
                    "@EndUserText.label": "DUMMY_COLUMN_TEXT2"
                },
                "SPRAS": {
                    "type": "DUMMY_TYPE3",
                    "length": 0,
                    "@EndUserText.label": "DUMMY_COLUMN_TEXT2"
                }
            }
        }
    }
}

new_columns = [
    {
        "name": "NEW_COLUMN",
        "type": "STRING",
        "precision": 255,
        "scale": 0,
        "@EndUserText.label": "New Column Label"
    },
    {
        "name": "NEW_COLUMN2",
        "type": "INTEGER",
        "precision": 10,
        "scale": 0,
        "@EndUserText.label": "New Column Label 2"
    }
]


def add_columns_to_elements(json_data, table_name, new_columns):
    """
    Fügt neue Spalten zum 'elements' Abschnitt eines bestimmten Tables im JSON hinzu.

    :param json_data: Das JSON-Datenobjekt, das die Tabelle und Elemente enthält.
    :param table_name: Der Name der Tabelle, zu der die Spalten hinzugefügt werden.
    :param new_columns: Eine Liste von Dictionaries, die die neuen Spalten beschreiben. 
                         Jede Spalte muss 'name', 'type', 'precision', 'scale' und 'label' enthalten.
    :return: Das aktualisierte JSON-Datenobjekt.
    """
    # Zugriff auf den Bereich der Tabelle und der Elemente im JSON
    if table_name in json_data['definitions']:
        print(f'Definitions: {json_data['definitions']}')
        table = json_data['definitions'][table_name]
        print(f'Table: {table}')
        elements = table['elements']
        print(f'Elements: {elements}')

        # Hinzufügen jeder neuen Spalte zum 'elements' Abschnitt
        for column in new_columns:
            # Jede neue Spalte ist ein Dictionary mit verschiedenen Eigenschaften
            # column_name = column['name']
            # elements[column_name] = {
            #     "type": column['type'],
            #     "precision": column['precision'],
            #     "scale": column['scale'],
            #     "@EndUserText.label": column['@EndUserText.label']
            # }
            column_name = column['FIELDNAME']
            elements[column_name] = {
                "@EndUserText.label": column['FIELDTEXT']
            }

        return json_data  # Rückgabe der aktualisierten JSON-Daten
    else:
        print(f"Table {table_name} not found in definitions.")
        return json_data  # Wenn der Tabellenname nicht existiert, bleibt das JSON unverändert


def update_column_value(json_data, table_name, column_name, new_value):
    # Überprüfen, ob die Tabelle im JSON existiert
    if table_name in json_data['definitions']:
        table = json_data['definitions'][table_name]

        # Überprüfen, ob die Spalte (Element) in der Tabelle existiert
        if column_name in table['elements']:
            column = table['elements'][column_name]

            # Jetzt den Wert der Spalte ändern
            # Beispiel: Wir ändern den `@EndUserText.label` Wert
            column['@EndUserText.label'] = new_value
            print(
                f"Column '{column_name}' in table '{table_name}' updated to: {new_value}")

            # Optional: Du kannst auch andere Werte wie 'type', 'precision', 'scale' ändern, je nach Bedarf
            # column['type'] = "NEU_TYP"
            # column['precision'] = 10
            # column['scale'] = 2

        else:
            print(f"Column '{column_name}' not found in table '{table_name}'")
    else:
        print(f"Table '{table_name}' not found in definitions")


def update_or_add_column(json_data, table_name, column_name, new_values):
    """
    Aktualisiert eine bestehende Spalte oder fügt eine neue Spalte hinzu, wenn diese noch nicht existiert.

    :param json_data: Das JSON-Datenobjekt
    :param table_name: Der Name der Tabelle, die bearbeitet werden soll
    :param column_name: Der Name der Spalte, die aktualisiert oder hinzugefügt werden soll
    :param new_values: Ein Dictionary mit den neuen Werten, die der Spalte zugewiesen werden sollen
    """
    # Überprüfen, ob die Tabelle existiert
    if table_name in json_data['definitions']:
        table = json_data['definitions'][table_name]

        # Überprüfen, ob die Spalte bereits existiert
        if column_name in table['elements']:
            # Die Spalte existiert, also update die Werte
            column = table['elements'][column_name]
            print(
                f"Updating column '{column_name}' in table '{table_name}'...")
            # Alle neuen Werte in der Spalte aktualisieren
            for key, value in new_values.items():
                column[key] = value
            print(f"Updated values for column '{column_name}': {new_values}")
        else:
            # Die Spalte existiert nicht, also füge sie hinzu
            print(
                f"Adding new column '{column_name}' to table '{table_name}'...")
            table['elements'][column_name] = new_values
            print(
                f"Added new column '{column_name}' with values: {new_values}")
    else:
        print(f"Table '{table_name}' not found in definitions")

def update_column_value_from_csv(json_data, table_name, column_name, new_value):
    # Überprüfen, ob die Tabelle im JSON existiert
    if table_name in json_data['definitions']:
        table = json_data['definitions'][table_name]

        # Überprüfen, ob die Spalte (Element) in der Tabelle existiert
        if column_name in table['elements']:
            column = table['elements'][column_name]

            # Jetzt den Wert der Spalte ändern
            # Beispiel: Wir ändern den `@EndUserText.label` Wert
            column['@EndUserText.label'] = new_value
            print(
                f"Column '{column_name}' in table '{table_name}' updated to: {new_value}")

            # Optional: Du kannst auch andere Werte wie 'type', 'precision', 'scale' ändern, je nach Bedarf
            # column['type'] = "NEU_TYP"
            # column['precision'] = 10
            # column['scale'] = 2

        else:
            print(f"Column '{column_name}' not found in table '{table_name}'")
    else:
        print(f"Table '{table_name}' not found in definitions")

# json_data = add_columns_to_elements(
#     json_template, "DUMMY_TABLE_NAME", new_columns)

# json_data = add_columns_to_elements(json_template, "DUMMY_TABLE_NAME", data_dict)
json_data = update_column_value_from_csv(json_template, "DUMMY_TABNAME", "AGR_NAME", data_dict)
# print(json.dumps(json_data, indent=4))
