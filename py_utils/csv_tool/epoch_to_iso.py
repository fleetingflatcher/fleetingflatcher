import csv
from datetime import datetime

def convert_to_iso(seconds):
    timestamp = datetime.utcfromtimestamp(seconds).isoformat() + 'Z'
    return timestamp

input_file = 'input.csv'
output_file = 'output.csv'

with open(input_file, 'r', newline='') as f:
    reader = csv.DictReader(f)
    header = reader.fieldnames
    header.insert(0, 'timestamp')
    data = list(reader)
    # print(data)

for row in data:
    row['timestamp'] = convert_to_iso(float(row['seconds']))
    row.pop('seconds')
    print(row)

header.remove('seconds')
with open(output_file, 'w', newline='') as f:    
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(data)

print("Conversion complete. Output saved to", output_file)