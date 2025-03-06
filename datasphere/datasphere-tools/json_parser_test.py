import csv
import json
import copy

class dspUtils:

    @staticmethod
    def map_csv_row_to_json_fields(row):
        """Mappt eine CSV-Zeile auf die JSON-Felder."""
        return {
            "tabname": f"TEST_{row['TABNAME']}",  # Prefix TEST_ hinzufügen
            "fieldname": row["FIELDNAME"],
            "datatype": row["DATATYPE"],
            "fieldtext": row["FIELDTEXT"]
        }


    @staticmethod
    def read_json_file(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"❌ Die Datei {json_file} wurde nicht gefunden.")
            return None
        except json.JSONDecodeError:
            print("❌ Fehler beim Dekodieren der JSON-Datei.")
            return None
        except Exception as e:
            print(f"❌ Ein unerwarteter Fehler ist aufgetreten: {e}")
            return None

    @staticmethod
    def write_json_file(json_data, json_file):
        try:
            with open(json_file, 'w', encoding='utf-8') as file:
                json.dump(json_data, file, ensure_ascii=False, indent=4)
            print(f"✅ Datei gespeichert: {json_file}")
        except Exception as e:
            print(f"❌ Fehler beim Speichern der Datei {json_file}: {e}")

    @staticmethod
    def parse_csv_to_json_structure(csv_file, template_file=None):
        tables = {}  # Dictionary für Tabellen-Strukturen

        json_template = None
        if template_file:
            json_template = dspUtils.read_json_file(template_file)
            if not json_template:
                return None  # Falls das Template fehlerhaft ist, abbrechen

        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')

            for row in reader:
                mapped_data = dspUtils.map_csv_row_to_json_fields(row)  # Mapping-Methode nutzen

                tabname = mapped_data["tabname"]
                fieldname = mapped_data["fieldname"]
                datatype = mapped_data["datatype"]
                fieldtext = mapped_data["fieldtext"]

                if tabname not in tables:
                    if json_template:
                        dummy_tabname = list(json_template["definitions"].keys())[0]
                        tables[tabname] = {
                            "definitions": {
                                tabname: copy.deepcopy(json_template["definitions"][dummy_tabname])
                            }
                        }
                        tables[tabname]["definitions"][tabname]["@EndUserText.label"] = tabname
                        tables[tabname]["definitions"][tabname]["elements"] = {}
                    else:
                        tables[tabname] = {
                            "definitions": {
                                tabname: {
                                    "kind": "entity",
                                    "@ObjectModel.modelingPattern": {"#": "DATA_STRUCTURE"},
                                    "@ObjectModel.supportedCapabilities": [{"#": "DATA_STRUCTURE"}],
                                    "@EndUserText.label": tabname,
                                    "elements": {}
                                }
                            }
                        }

                tables[tabname]["definitions"][tabname]["elements"][fieldname] = {
                    "type": datatype,
                    "@EndUserText.label": fieldtext
                }

        return tables


    @staticmethod
    def parse_csv_to_json_transformation_flow(csv_file, template_file=None):
        # tables = {}  # Dictionary für Tabellen-Strukturen

        # Falls ein Template existiert, lade es ein
        # json_template = None
        # if template_file:
        #     json_template = dspUtils.read_json_file(template_file)
        #     if not json_template:
        return None  # Falls das Template fehlerhaft ist, abbrechen

    @staticmethod
    def create_lt_from_csv(csv_file):
        """Erstellt eine JSON-Struktur aus einer CSV-Datei und gibt sie als Dictionary zurück."""
        return dspUtils.parse_csv_to_json_structure(csv_file)

    @staticmethod
    def create_json_files_from_csv(csv_file, template_file, dsp_object_type=None):

        if dsp_object_type==None:
            raise Exception('No Type specified')
        else:
            # Passende Parsing-Methode auswählen
            if dsp_object_type == "TABLE":
                tables = dspUtils.parse_csv_to_json_structure(csv_file, template_file)
                        # print(f'Tabelle: {tables}')
            if tables:
                for tabname, json_data in tables.items():
                    file_name = f"{tabname}.json"
                    dspUtils.write_json_file(json_data, file_name)
            elif dsp_object_type == "TRANSFORMATION_FLOW":
                json_data = dspUtils.parse_csv_to_json_transformation_flow(csv_file, template_file)
            else:
                print(f"⚠️ Unbekannter Objekttyp: {dsp_object_type}")
        """Erstellt JSON-Dateien pro Tabelle aus einer CSV-Datei."""

csv_file = r"datasphere/datasphere-tools/templates/CSV_Template.csv"
template_file = r"datasphere/datasphere-tools/templates/local_table.json"

dspUtils.create_json_files_from_csv(csv_file, template_file, 'TABLE')