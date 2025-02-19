import subprocess

dsp_output_path = r"datasphere\datasphere-tools\dsp_downloads"
dsp_technical_name = input("Please provide a technical name : ")
dsp_accept = input("Please provide accept parameter[optional] : ") # E.g.: "application/vnd.sap.datasphere.object.content.design-time+json"

if dsp_accept:
    command = f'datasphere objects local-tables read --technical-name {dsp_technical_name} --space PLAYGROUND --accept {dsp_accept} --output {dsp_output_path}\{dsp_technical_name}.json'
    subprocess.run(command, shell=True)
    print(command)
else: 
    command = f'datasphere objects local-tables read --technical-name {dsp_technical_name} --space PLAYGROUND --output {dsp_output_path}\{dsp_technical_name}.json'
    subprocess.run(command, shell=True)
    print(command)