import subprocess
import json
import pandas as pd
import re
import inquirer
import csv
import copy

class dspUtils:

    def run_command(command):
        print(f'Command: {command}')
        subprocess.run(command, shell=True)

    def logoutlogin(dsp_logon_data_file):
        # -----------------------------------------------------------
        # Read host
        # -----------------------------------------------------------
        # dsp_host=dspUtils.read_var_from_file(dsp_logon_data_file,'dsp_host')
        # Read host and credentials
        dsp_logon_data = r"datasphere\datasphere-tools\dsp_config\dsp_logon_data.json"

        try:
            with open(dsp_logon_data, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
        except FileNotFoundError:
            print("The file was not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        dsp_host = json_data["dsp_host"]
        # -----------------
        # print versions of relevant components
        # -----------------
        dspUtils.run_command('node --version')
        dspUtils.run_command('npm --version')
        dspUtils.run_command('datasphere -version')

        # -----------------------------------------------------------
        # CLI logon procedure with oAuth authentication to DSP CLI
        # -----------------------------------------------------------

        # logout is needed to have the login consider new creds file, e.g., in case it is replaced with new client id/secret
        dspUtils.run_command('datasphere logout')

        # login
        dspUtils.run_command(f'datasphere login --host {dsp_host} --secrets-file {dsp_logon_data_file}')

        # set global host
        dspUtils.run_command(f'datasphere config host set {dsp_host}')

        # Optional command to debug or to get the access and refresh token to avoid login command (see header comments)
        dspUtils.run_command('datasphere config secrets show')

    def download_json():
        dsp_output_path = r"datasphere\datasphere-tools\dsp_files\dsp_downloads"
        dsp_technical_name = input("Please provide a technical name : ")
        dsp_object_type = input("Please provide an object type[default: local-tables] : ").strip() or 'local-tables'
        dsp_space = input("Please provide a space name[default: INGESTION_001] : ").strip() or 'INGESTION_001'
        dsp_accept = input("Please provide accept parameter[optional] : ") 
            # E.g.: 
            # "application/vnd.sap.datasphere.object.content+json"             (default)
            # "application/vnd.sap.datasphere.object.content.design-time+json" (Includes _meta information like folder dependency)
            # "application/vnd.sap.datasphere.object.content.run-time+json"    (like default)

        if dsp_accept:
            command = f'datasphere objects {dsp_object_type}  read --technical-name {dsp_technical_name} --space {dsp_space} --accept {dsp_accept} --output "{dsp_output_path}\\{dsp_technical_name}.json" --verbose'
        else: 
            command = f'datasphere objects {dsp_object_type}  read --technical-name {dsp_technical_name} --space {dsp_space} --output "{dsp_output_path}\\{dsp_technical_name}.json" --verbose'

        dspUtils.run_command(command)

    def download_json_interactive():
        dsp_output_path = r"datasphere\datasphere-tools\dsp_files\dsp_downloads"

        # Interactive Terminal prompts with menu selection via arrow keys on keyboard
        dsp_technical_name = inquirer.prompt(
            [
                inquirer.Text(
                    "dsp_technical_name", message="Please provide a technical name"
                )
            ]
        )["dsp_technical_name"]

        dsp_object_type = inquirer.prompt(
            [
                inquirer.List(
                    "dsp_object_type",
                    message="Please provide an object type",
                    choices=[
                        "local-tables",
                        "replication-flows",
                        "transformation-flows",
                    ],
                    default="local-tables",
                )
            ]
        )["dsp_object_type"]

        dsp_space = inquirer.prompt(
            [
                inquirer.List(
                    "dsp_space",
                    message="Please provide a space name",
                    choices=[
                        "INGESTION_001",
                        "OUTBOUND_001",
                        "PLAYGROUND",
                    ],
                    default="INGESTION_001",
                )
            ]
        )["dsp_space"]

        dsp_accept = inquirer.prompt(
            [
                inquirer.List(
                    "dsp_accept",
                    message="Please provide accept parameter (optional)",
                    choices=[
                        "None",  # Easy selection. In the background Datasphere uses its default
                        "application/vnd.sap.datasphere.object.content+json", # Default used in Datasphere
                        "application/vnd.sap.datasphere.object.content.design-time+json",
                        "application/vnd.sap.datasphere.object.content.run-time+json",
                    ],
                    default="None",
                )
            ]
        )["dsp_accept"]

        if dsp_accept != "None":
            command = f'datasphere objects {dsp_object_type} read --technical-name {dsp_technical_name} --space {dsp_space} --accept {dsp_accept} --output "{dsp_output_path}\\{dsp_technical_name}.json" --verbose'
        else:
            command = f'datasphere objects {dsp_object_type} read --technical-name {dsp_technical_name} --space {dsp_space} --output "{dsp_output_path}\\{dsp_technical_name}.json" --verbose'

        dspUtils.run_command(command)

    def upload_json():
        dsp_file_path = r"datasphere\datasphere-tools\dsp_files\dsp_uploads"
        dsp_technical_name = input("Please provide a technical name : ")
        dsp_space = input("Please provide a space name[default: PLAYGROUND] : ").strip() or 'PLAYGROUND'
        dsp_object_type = input("Please provide the object type [default: local-tables] : ").strip() or 'local-tables'
        dsp_crud_type = input("Please provide the update type [create] [update] : ")      
        dsp_upload_file = input("Please provide a file name : ")

        command = f'datasphere objects {dsp_object_type} {dsp_crud_type} --technical-name {dsp_technical_name} --space {dsp_space} --file-path "{dsp_file_path}\\{dsp_upload_file}" --verbose'
        print(f'Datasphere command: {command}')
        if input("Confirm [Y or N]: ") == 'Y':
            dspUtils.run_command(command)
        else: 
            print("Upload canceled")

    def upload_json_interactive():
        dsp_file_path = r"datasphere\datasphere-tools\dsp_files\dsp_uploads"

        # Interactive Terminal prompts with menu selection via arrow keys on keyboard
        dsp_technical_name = inquirer.prompt([
            inquirer.Text('dsp_technical_name', message="Please provide a technical name")
        ])['dsp_technical_name']
        
        dsp_space = inquirer.prompt([
            inquirer.List('dsp_space',
                        message="Please provide a space name",
                        choices=['PLAYGROUND', 'INGESTION_001', 'OUTBOUND_001'],
                        default='PLAYGROUND')
        ])['dsp_space']
        
        dsp_object_type = inquirer.prompt([
            inquirer.List('dsp_object_type',
                        message="Please provide the object type",
                        choices=['local-tables', 'replication-flows', 'transformation-flows'],
                        default='local-tables')
        ])['dsp_object_type']
        
        dsp_crud_type = inquirer.prompt([
            inquirer.List('dsp_crud_type',
                        message="Please provide the update type",
                        choices=['create', 'update'],
                        default='create')
        ])['dsp_crud_type']
        
        dsp_upload_file = inquirer.prompt([
            inquirer.Text('dsp_upload_file', message="Please provide a file name")
        ])['dsp_upload_file']
        
        command = f'datasphere objects {dsp_object_type} {dsp_crud_type} --technical-name {dsp_technical_name} --space {dsp_space} --file-path "{dsp_file_path}\\{dsp_upload_file}" --verbose'
        
        # User confirmation
        confirm = inquirer.prompt([
            inquirer.Confirm('confirm', message="Confirm", default=True)
        ])['confirm']
        
        if confirm:
            print(f'Datasphere command: {command}')
            subprocess.run(command, shell=True)
        else:
            print("Upload canceled")

    def read_json_file(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print("The file was not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def write_json_file(json_data, json_file):
        try:
            with open(json_file, 'w', encoding='utf-8') as file:
                json.dump(json_data, file, ensure_ascii=False, indent=4)
            print(f"Data successfully written to {json_file}.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def read_csv_file(csv_file):
        try:
            return pd.read_csv(csv_file, sep=";")
        except FileNotFoundError:
            print(f"The file {csv_file} was not found.")
        except pd.errors.EmptyDataError:
            print("The file is empty.")
        except pd.errors.ParserError:
            print("There was a problem parsing the file (possibly incorrect format).")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def search_json(data, pattern, parent_key=""):
        # If data is a dictionary
        if isinstance(data, dict):
            for key, value in data.items():
                # Create the full key path
                full_key = f"{parent_key}.{key}" if parent_key else key
                
                # Check if the current key matches the wildcard
                if re.search(pattern, full_key):  # `re.search` looks for matches anywhere in the string
                    yield full_key, value  # If the key matches, return it along with its value

                # Recursive call if the value is a dictionary or list
                if isinstance(value, (dict, list)):
                    yield from dspUtils.search_json(value, pattern, full_key)  # Pass the current key as the parent path    
        # If data is a list, iterate through the list
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                # Create a new key path for lists by adding the index
                full_key = f"{parent_key}[{idx}]"
                yield from dspUtils.search_json(item, pattern, full_key)

    # Helper function to update nested JSON data
    def update_json(data, key, value):
        # Temporarily replace @EndUserText.label with a placeholder
        temp_key = key.replace('@EndUserText.label', '@EndUserText_label')  
        # Split the key by dots, but ignore @EndUserText_label
        keys = temp_key.split('.')  
        # Ensure that we replace the placeholder back to @EndUserText.label
        keys = [key.replace('@EndUserText_label', '@EndUserText.label') for key in keys]
        print("Keys after split: " + str(keys))
        print("Value to update :" + str(value))
        
        for k in keys[:-1]:
            # If the value is a dictionary
            if isinstance(data, dict):
                if k not in data:
                    raise KeyError(f"Key '{k}' is missing in the data")
                # print(f"Processing: {data} -> {k}")
                data = data[k]  # Continue in the nested structure
            # If the value is a list
            elif isinstance(data, list):
                try:
                    index = int(k)  # Try to interpret the key as an index
                    data = data[index]  # Move to the list at the specified position
                except (ValueError, IndexError):
                    raise KeyError(f"The index '{k}' is invalid for the list")
            else:
                raise TypeError(f"Expected a dictionary or list, but {type(data)} was found at key '{k}'")

        # Set the value for the last key
        if isinstance(data, dict):
            data[keys[-1]] = value
        else:
            raise TypeError(f"Expected a dictionary at the end, but {type(data)} was found at key '{keys[-1]}'")
        
    def create_lt_from_csv(csv_file):
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")

            local_table = {
                "definitions":{

                }
            }

            for row in reader:
                tabname = row["TABNAME"]
                fieldname = row["FIELDNAME"]
                datatype = row["DATATYPE"]
                fieldtext = row["FIELDTEXT"]
                tabname = f"TEST_{tabname}"
                if tabname not in local_table["definitions"]:
                    local_table["definitions"][tabname] = {
                        "kind": "entity",
                        "@ObjectModel.modelingPattern": {"#": "DATA_STRUCTURE"},
                        "@ObjectModel.supportedCapabilities": [{"#": "DATA_STRUCTURE"}],
                        "@EndUserText.label": tabname,
                        "elements": {},
                    }

                local_table["definitions"][tabname]["elements"][fieldname] = {
                    "type": datatype,
                    "@EndUserText.label": fieldtext,
                }
            return local_table
    
    def create_json_files_from_csv(csv_file, template_file):
        tables = {}  # Dictionary für Tabellen-Strukturen
        json_template = dspUtils.read_json_file(template_file)
        # CSV-Datei lesen
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')

            for row in reader:
                tabname = row["TABNAME"]
                fieldname = row["FIELDNAME"]
                datatype = row["DATATYPE"]
                fieldtext = row["FIELDTEXT"]

                # Falls die Tabelle noch nicht existiert, erstelle eine Kopie des Templates
                if tabname not in tables:
                    dummy_tabname = list(json_template["definitions"].keys())[0]  # "DUMMY_TABNAME"
                    tables[tabname] = {
                        "definitions": {
                            tabname: copy.deepcopy(json_template["definitions"][dummy_tabname])
                        }
                    }
                    # Setze das Tabellen-Label
                    tables[tabname]["definitions"][tabname]["@EndUserText.label"] = tabname
                    # Leere die "elements"-Struktur
                    tables[tabname]["definitions"][tabname]["elements"] = {}

                # Element zur Tabelle hinzufügen
                tables[tabname]["definitions"][tabname]["elements"][fieldname] = {
                    "type": datatype,
                    "@EndUserText.label": fieldtext
                }

        # JSON-Dateien für jede Tabelle speichern
        for tabname, json_data in tables.items():
            file_name = f"{tabname}.json"
            with open(file_name, "w", encoding="utf-8") as json_file:
                json.dump(json_data, json_file, indent=4, ensure_ascii=False)
            print(f"✅ Datei erstellt: {file_name}")