from dsp_utils import dspUtils as du

# File
csv_filename = r"datasphere\datasphere-tools\dsp_files\dsp_source_metadata\B25_Export_Metadata_ZDS_AGR_USERS.csv"

du.create_json_files_from_csv(csv_filename, dsp_object_type="LOCAL_TABLE")