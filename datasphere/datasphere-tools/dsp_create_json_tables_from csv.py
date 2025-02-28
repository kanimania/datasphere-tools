from dsp_utils import dspUtils as du

# Files
csv_filename = r"datasphere\datasphere-tools\dsp_files\dsp_source_metadata\B25_Export_Metadata_ZDS_AGR_USERS.csv"
template_filename = r"datasphere\datasphere-tools\templates\local_table.json"

du.create_json_files_from_csv(csv_filename, template_filename)