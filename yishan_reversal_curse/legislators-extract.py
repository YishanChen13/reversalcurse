import csv

def extract_columns(input_file, output_file, columns):
    with open(input_file, mode='r', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=columns)

        writer.writeheader()
        for row in reader:
            writer.writerow({col: row[col] for col in columns})

input_csv = 'legislators-current.csv'
output_csv = 'legislators-names.csv'  
columns_to_keep = ['full_name']

extract_columns(input_csv, output_csv, columns_to_keep)
