import subprocess
import json
import inquirer
import csv
import copy
from pathlib import Path

class dspUtils:

    @staticmethod
    def run_command(command):
        print(f"🔹 Running: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error executing command: {result.stdout}")
            print(f"❌ Additional error log: {result.stderr}" ) if result.stderr else None
        else:
            print(f"✅ Command executed successfully: {result.stdout}")
        return result.returncode

    @staticmethod
    def logoutlogin():
        # -----------------------------------------------------------
        # Read host
        # -----------------------------------------------------------
        dsp_logon_data_file = Path(
            r"datasphere\datasphere-tools\dsp_config\dsp_logon_data.json"
        )
        # dsp_host = dspUtils.read_var_from_file(dsp_logon_data_file,'host')

        # -----------------------------------------------------------
        # CLI logon procedure with oAuth authentication to DSP CLI
        # -----------------------------------------------------------

        # logout is needed to have the login consider new creds file, e.g., in case it is replaced with new client id/secret
        dspUtils.run_command("datasphere logout")

        # login
        # dspUtils.run_command(f'datasphere login --host {dsp_host} --secrets-file {dsp_logon_data_file} --verbose')
        dspUtils.run_command(
            f"datasphere login --options-file {dsp_logon_data_file} --verbose"
        )

        # set global host
        # dspUtils.run_command(f'datasphere config host set {dsp_host}')
        # check global host
        # dspUtils.run_command("datasphere config host show")

        # Optional command to debug or to get the access and refresh token to avoid login command
        # dspUtils.run_command('datasphere config secrets show')

    @staticmethod
    def read_var_from_file(file_path, var_name):
        data = dspUtils.read_json_file(file_path)
        if var_name in data:
            return data[var_name]
        else:
            return None

    @staticmethod
    def download_json():
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
                        "application/vnd.sap.datasphere.object.content+json",  # Default used in Datasphere
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

        # result = dspUtils.run_command(command)
        # print(f"✅ File successfully written to: {dsp_output_path}\\{dsp_technical_name}.json") if result == 0 else None

    @staticmethod
    def upload_json():
        dsp_file_path = r"datasphere\datasphere-tools\dsp_files\dsp_uploads"

        # Interactive Terminal prompts with menu selection via arrow keys on keyboard
        dsp_technical_name = inquirer.prompt(
            [
                inquirer.Text(
                    "dsp_technical_name", message="Please provide a technical name"
                )
            ]
        )["dsp_technical_name"]

        dsp_space = inquirer.prompt(
            [
                inquirer.List(
                    "dsp_space",
                    message="Please provide a space name",
                    choices=["PLAYGROUND", "INGESTION_001", "OUTBOUND_001"],
                    default="PLAYGROUND",
                )
            ]
        )["dsp_space"]

        dsp_object_type = inquirer.prompt(
            [
                inquirer.List(
                    "dsp_object_type",
                    message="Please provide the object type",
                    choices=[
                        "local-tables",
                        "replication-flows",
                        "transformation-flows",
                    ],
                    default="local-tables",
                )
            ]
        )["dsp_object_type"]

        dsp_crud_type = inquirer.prompt(
            [
                inquirer.List(
                    "dsp_crud_type",
                    message="Please provide the update type",
                    choices=["create", "update"],
                    default="create",
                )
            ]
        )["dsp_crud_type"]

        dsp_upload_file = inquirer.prompt(
            [inquirer.Text("dsp_upload_file", message="Please provide a file name")]
        )["dsp_upload_file"]

        command = f'datasphere objects {dsp_object_type} {dsp_crud_type} --technical-name {dsp_technical_name} --space {dsp_space} --file-path "{dsp_file_path}\\{dsp_upload_file}" --verbose'

        # User confirmation
        confirm = inquirer.prompt(
            [inquirer.Confirm("confirm", message="Confirm", default=True)]
        )["confirm"]

        if confirm:
            print(f"Datasphere command: {command}")
            subprocess.run(command, shell=True)
        else:
            print("Upload canceled")

    @staticmethod
    def read_json_file(json_file):
        try:
            with open(json_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"❌ File not found: {json_file}")
        except json.JSONDecodeError as e:
            print(f"❌ JSON Decode Error in {json_file}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        return None

    @staticmethod
    def write_json_file(json_data, json_file):
        try:
            with open(json_file, "w", encoding="utf-8") as file:
                json.dump(json_data, file, ensure_ascii=False, indent=4)
            print(f"✅ Data successfully written to {json_file}.")
        except Exception as e:
            print(f"❌ An error occurred: {e}")

    @staticmethod
    def read_csv_file(csv_file: Path) -> list[dict]:
        try:
            with open(csv_file, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file, delimiter=";")
                return list(reader)  # Store all rows in memory before closing the file
        except FileNotFoundError:
            # print(f"❌ The file {csv_file} was not found.")
            # return None
            raise FileNotFoundError(f"❌ The file {csv_file} was not found.")
        except csv.Error as e:
            # print(f"❌ CSV Error: {e}")
            # return None
            raise ValueError(f"❌ CSV Error: {e}")

    @staticmethod
    def csv_column_name_translation():
        # Values are the names of the csv columns
        return {
            "tabname": "TABNAME",
            "fieldname": "FIELDNAME",
            "datatype": "DATATYPE",
            "fieldtext": "FIELDTEXT",
        }

    @staticmethod
    def parse_csv_to_json_local_table(csv_file):
        json_dict = {}  # Dictionary for local_tables

        # Define the template file for tables
        template_file: Path = Path(r"datasphere/datasphere-tools/templates/local_table.json")
        if template_file:
            json_template = dspUtils.read_json_file(template_file)
            if not json_template:
                return None  # If issues with template

        # Read CSV File
        csv_data = dspUtils.read_csv_file(csv_file)
        if csv_data is None:
            return None  # Exit if the CSV file could not be read

        csv_columns = dspUtils.csv_column_name_translation()
        for row in csv_data:

            tabname = f"TEST_{row[csv_columns["tabname"]]}"
            fieldname = row[csv_columns["fieldname"]]
            datatype = row[csv_columns["datatype"]]
            fieldtext = row[csv_columns["fieldtext"]]

            if tabname not in json_dict:
                if json_template:
                    dummy_tabname = list(json_template["definitions"].keys())[0]
                    json_dict[tabname] = {
                        "definitions": {
                            tabname: copy.deepcopy(
                                json_template["definitions"][dummy_tabname]
                            )
                        }
                    }
                    json_dict[tabname]["definitions"][tabname][
                        "@EndUserText.label"
                    ] = tabname
                    json_dict[tabname]["definitions"][tabname]["elements"] = {}
            # Adding columns from csv
            json_dict[tabname]["definitions"][tabname]["elements"][fieldname] = {
                "type": datatype,
                "@EndUserText.label": fieldtext,
            }

        return json_dict

    @staticmethod
    def parse_csv_to_json_transformation_flow(csv_file, template_file=None):
        # TBD
        return None  # Abort if error

    @staticmethod
    def create_json_files_from_csv(csv_file, dsp_object_type=None):
        # File Output Path
        file_path = r"datasphere/datasphere-tools/local Tests/"
        # Creates JSON files from a CSV file based on the object type.
        if dsp_object_type is None:
            raise ValueError(
                "No Datasphere object type specified. Please provide a valid type."
            )
        # Choose the correct parsing method
        if dsp_object_type == "LOCAL_TABLE":
            json_dict = dspUtils.parse_csv_to_json_local_table(csv_file)
            # If parsing was successful, write each JSON file
        elif dsp_object_type == "TRANSFORMATION_FLOW":
            json_dict = dspUtils.parse_csv_to_json_transformation_flow(csv_file)
        else:
            print(f"⚠️ Unknown object type: {dsp_object_type}")
        # Write Json Files
        if json_dict:
            for dsp_object, json_data in json_dict.items():
                file_name = f"{file_path}{dsp_object}.json"
                dspUtils.write_json_file(json_data, file_name)
        else:
            print("❌ No data to write.")
            return

    @staticmethod
    def update_dsp_column_labels_from_csv(csv_file: Path, json_files: list[str]) -> None:
        file_path: Path = Path(r"datasphere\datasphere-tools\local tests")
        json_dict: dict[str, dict] = {}  # Dictionary containing content of json_file(s) for update
        updated_tables: dict[str, bool] = {}

        # Read CSV File
        csv_data: list[dict] = dspUtils.read_csv_file(csv_file)
        csv_columns: dict = dspUtils.csv_column_name_translation()

        # Read Json File(s)
        for filename in json_files:
            updated_tables[filename] = False # Logic which deals with existing values in Json but not in CSV
            file: Path = file_path / filename
            if not file.exists(): 
                raise FileNotFoundError(f"❌ File does not exist: {file}") # Redundant? Handling better in read_json_file?

            json_dict[filename] = dspUtils.read_json_file(file)
            if json_dict[filename] is None:
                continue

            # filtered_rows: filter = filter(lambda row: f"{row[csv_columns['tabname']]}.json" == filename, csv_data) # Filter CSV File only with matching Json Tables
            filtered_rows: list[dict] = [row for row in csv_data if f"{row[csv_columns['tabname']]}.json" == filename] # easier for small CSV'S and returns list
            for row in filtered_rows:

                tablename: str = row[csv_columns["tabname"]]
                fieldname: str = row[csv_columns["fieldname"]]
                fieldtext: str = row[csv_columns["fieldtext"]]

                if f"{tablename}.json" not in json_dict: # Logic which deals with existing values in CSV but not in Json
                    continue
                if tablename in json_dict[f"{tablename}.json"]["definitions"]: # .get("definitions", {}):
                    # elements = json_dict[f"{tablename}.json"]["definitions"][tablename].setdefault("elements", {})
                    elements = json_dict[f"{tablename}.json"]["definitions"][tablename]["elements"]
                    if fieldname in elements:
                        print(f"🔄 Updating field {fieldname} in {tablename}.json")
                        elements[fieldname]["@EndUserText.label"] = fieldtext
                        updated_tables[f"{tablename}.json"] = True

        if json_dict:
            for file, json_data in json_dict.items():
                if updated_tables[file] == True:
                    file_name: Path = file_path / file.replace(".json", "_updated.json")
                    dspUtils.write_json_file(json_data, file_name)
        else:
            print("❌ No data to write.")

if __name__ == "__main__":
    csv_file: Path = Path(r"datasphere/datasphere-tools/templates/CSV_Template.csv")
    dspUtils.update_dsp_column_labels_from_csv(csv_file, ["TEST_ZOXB250146.json", "TEST_CLuI.json"])
