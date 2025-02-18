import subprocess

dsp_technical_name = input("Please provide a technical name : ")
dsp_output_path = r"datasphere\datasphere-tools\dsp_downloads"

command = f'datasphere objects local-tables read --technical-name {dsp_technical_name} --space INGESTION_001 --output {dsp_output_path}\{dsp_technical_name}.json'
subprocess.run(command, shell=True)