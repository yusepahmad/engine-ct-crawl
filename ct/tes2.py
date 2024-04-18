import pandas as pd
import re

file_csv = 'https://www.ctdatacollaborative.org/sites/g/files/tmzbdl2011/files/visualization-chart-source/fl_total1_1.csv'

field = file_csv.split('%20')[0].split('/')[-1]
df = pd.read_csv(file_csv)

json_output = df.to_dict(orient='records')

print(json_output)