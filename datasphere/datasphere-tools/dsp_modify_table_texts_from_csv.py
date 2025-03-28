from dsp_utils import dspUtils as du
from pathlib import Path

csv_file: Path = Path(r"datasphere/datasphere-tools/templates/CSV_Template.csv")
du.update_dsp_column_labels_from_csv(csv_file, ["TEST_CLI.json"])