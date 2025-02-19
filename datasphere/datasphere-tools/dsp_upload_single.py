import subprocess
import json

# Read host and credentials
dsp_logon_data = r"datasphere\datasphere-tools\dsp_logon_data.json"

try:
    with open(dsp_logon_data, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
except FileNotFoundError:
    print("The file was not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

dsp_host  = json_data["dsp_host"]

# Default upload file
# dsp_upload_file = r"C:\Users\demlotter\OneDrive - Brenntag\Datasphere\CLI Development\Python Workspace\datasphere\datasphere-tools\Local Tests\Target Data.json"
# dsp_technical_name = input("Please provide a technical name : ")
dsp_technical_name = "TEST_CLI"
dsp_upload_file = r"datasphere\datasphere-tools\Local Tests\Target Data.json"

# Test
command = f'datasphere objects local-tables create --technical-name {dsp_technical_name} --space PLAYGROUND --file-path "{dsp_upload_file}" --verbose'
subprocess.run(command, shell=True)
print(command)

# Run datasphere-cli command (static)
# command = f'datasphere objects local_tables create --technical-name TEST_CLI --space PLAYGROUND --file-path {dsp_upload_file} --verbose'
# subprocess.run(command, shell=True)

# Run datasphere-cli command (dynamic)
# dsp_object_type = input("Please provide the object type [local_tables] [replication_flows] : ")
# dsp_space = input("Please provide the space name : ")
# dsp_update_type = input("Please provide the update type [create] [update] : ")
# dsp_technical_name = input("Please provide the technical-name : ")
# print(f'datasphere objects local_tables {dsp_update_type} --technical-name {dsp_technical_name} --space {dsp_space} --file-path {dsp_upload_file} --verbose')
# command = f'datasphere objects local_tables {dsp_update_type} --technical-name {dsp_technical_name} --space {dsp_space} --file-path {dsp_upload_file} --verbose'
# subprocess.run(command, shell=True)