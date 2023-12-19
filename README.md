## csv_file_analyzer
This script processes CSV files, providing various statistics and analyses. It supports both single files and all files in a directory.

##### Features

- **Primary Context Column:** Specify the primary context column using the `-c` or `--primary_context_column` argument.
- **Matching Context Column:** Optionally specify a matching context column using the `-m` or `--matching_context_column` argument in the format `COLUMN=VALUE`.
- **Results:** The script outputs JSON results to the console and a CSV file (`complete_analysis.txt`) with detailed analysis for each processed file.


##### Directory Processing
```
python script.py -d input_directory -c 2
```


##### Matching Context Value
```
python script.py -f input_file.csv -c 2 -m 3=5
```


##### Output
Results are displayed on the console in JSON format and saved to complete_analysis.txt in CSV format.

##### Additional Notes
For the matching context column, provide the column number and value in the format COLUMN=VALUE.



##### Requirements

- Python 3.x
- Libraries: `csv`, `json`, `argparse`, `time`, `os`

#####  Usage

##### SYNTAX
```
python csv_file_analyzer.py -f somefile.csv [-c 2] [-m 3=5] | -d input_directory [-c 2] [-m 3=5]
```

##### Single File Processing
```bash
python csv_file_analyzer.py -f input_file.csv -c 2 -m 3=4
```


##### Processing all files in a directory
```bash
python csv_file_analyzer.py -d path_to_some_directory -c 2 -m3=0
```
