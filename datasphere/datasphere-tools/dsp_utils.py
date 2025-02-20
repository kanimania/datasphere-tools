import subprocess
import json

class dspUtils:
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
            print(f'Datasphere command: {command}')
            subprocess.run(command, shell=True)
        else: 
            command = f'datasphere objects {dsp_object_type}  read --technical-name {dsp_technical_name} --space {dsp_space} --output "{dsp_output_path}\\{dsp_technical_name}.json" --verbose'
            print(f'Datasphere command: {command}')
            subprocess.run(command, shell=True)
    
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
            subprocess.run(command, shell=True)
        else: 
            print("Upload canceled")

    def run_command(command):
        print(command)
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