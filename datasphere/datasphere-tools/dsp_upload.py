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
print(f'Host: {dsp_host}')

dsp_space  = json_data["dsp_space"]
print(f'Space: {dsp_space}')

# Default upload file
dsp_upload_file = r"datasphere\datasphere-tools\Local Tests\Target Data.json"

# command = f'datasphere objects local_tables create --technical-name TEST_CLI --space {dsp_space} --file-path {dsp_upload_file} --verbose'
# subprocess.run(command, shell=True)

# subprocess.run(["powershell", "/c", "node -v"], shell=False)
# C:\\Users\\demlotter\\OneDrive - Brenntag\\Datasphere\\CLI Development\node-v22.13.1-win-x64\


# CRUD JSON commands:
# datasphere objects local-tables create --space INGESTION_001 --technical-name TEST_CLI --file-path "C:\Users\demlotter\OneDrive - Brenntag\Datasphere\CLI Development\Python Workspace\datasphere\datasphere-tools\Templates\local_table_delta_test.json"
# datasphere objects local-tables update --space INGESTION_001 --technical-name TEST_CLI --file-path "C:\Users\demlotter\OneDrive - Brenntag\Datasphere\CLI Development\Python Files\Target JSON.json"
# datasphere objects local-tables read   --space INGESTION_001 --technical-name TEST_CLI --output "C:\Users\demlotter\OneDrive - Brenntag\Datasphere\CLI Development\Python Workspace\datasphere\datasphere-tools\Templates\local_table.json"


# datasphere objects local-tables read --space PLAYGROUND --technical-name Template_Table --output "C:\Users\demlotter\OneDrive - Brenntag\Datasphere\CLI Development\Python Workspace\datasphere\datasphere-tools\Templates\Template_Table.json"
# datasphere objects local-tables create --space PLAYGROUND --technical-name Template_Table2 --file-path "C:\Users\demlotter\OneDrive - Brenntag\Datasphere\CLI Development\Python Workspace\datasphere\datasphere-tools\Templates\local_table_delta_test.json"