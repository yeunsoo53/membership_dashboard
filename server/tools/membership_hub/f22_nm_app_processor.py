import csv, json, sys

def process_data(csv_file_path, json_file_path):
    try:
        data = []
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                json_row = {}

                for key, value in row.items():
                    print(f"Key: {key} Value: {value}")
                    if key in ['Name', 'UIN', 'Email', 'Major']:
                        json_row[key] = value
                    elif key == 'Grad':
                        grad_class = value.split()

                        json_row['Grad Semester'] = grad_class[0]
                        json_row['Grad Year'] = int(grad_class[1])
                    else:
                        continue

                json_row['Admission'] = True

                print(f"After setting admission: {json_row}")

                data.append(json_row)

        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)

        print("Successfully converted")

    except Exception as e:
        print(f"Error opening file: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python csv_to_json.py input.csv output.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    process_data(input_file, output_file)