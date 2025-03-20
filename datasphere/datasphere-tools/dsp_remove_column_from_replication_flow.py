from dsp_utils import dspUtils as du
from pathlib import Path

output_path: Path = Path(r"datasphere\datasphere-tools\dsp_files\dsp_uploads")
file: Path = Path(r"datasphere\datasphere-tools\dsp_files\dsp_downloads\SD_BX_RF_E_Purchasing.json")
du.remove_column_from_replication_tasks(json_file=file,column_name="WKURS",output_folder=output_path)