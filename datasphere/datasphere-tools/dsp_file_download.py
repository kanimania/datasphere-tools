import subprocess

dsp_output_path = r"datasphere\datasphere-tools\dsp_files\dsp_downloads"
dsp_technical_name = input("Please provide a technical name : ")
dsp_accept = input("Please provide accept parameter[optional] : ") 
    # E.g.: 
    # "application/vnd.sap.datasphere.object.content+json"             (default)
    # "application/vnd.sap.datasphere.object.content.design-time+json" (Includes _meta information like folder dependency)
    # "application/vnd.sap.datasphere.object.content.run-time+json"    (like default)

if dsp_accept:
    command = f'datasphere objects local-tables read --technical-name {dsp_technical_name} --space PLAYGROUND --accept {dsp_accept} --output "{dsp_output_path}\\{dsp_technical_name}.json" --verbose'
    print(command)
    subprocess.run(command, shell=True)
else: 
    command = f'datasphere objects local-tables read --technical-name {dsp_technical_name} --space PLAYGROUND --output "{dsp_output_path}\\{dsp_technical_name}.json" --verbose'
    print(command)
    subprocess.run(command, shell=True)