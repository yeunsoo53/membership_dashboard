import json
import csv
import copy
import os

def update_admission(applicants_file, admitted_csv_file, output_file):
    try:
        # Load the main applicants data
        with open(applicants_file, 'r') as f:
            applicants = json.load(f)
        
        # Load the admitted UINs from CSV
        admitted_uins = set()
        with open(admitted_csv_file, 'r') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                admitted_uins.add(row["uin"])
        
        # Process each applicant
        updated_applicants = []
        found_admitted_uins = set()
        for applicant in applicants:
            # Create a deep copy to avoid modifying the original
            updated_applicant = copy.deepcopy(applicant)
            
            # Update admission status
            if updated_applicant["UIN"] in admitted_uins:
                updated_applicant["Admission"] = True
                found_admitted_uins.add(updated_applicant["UIN"])
                print(f"Set admission status to true for {updated_applicant.get('Name')} ({updated_applicant['UIN']})")
            else:
                updated_applicant["Admission"] = False
            
            updated_applicants.append(updated_applicant)

        #output admitted uins that aren't found in the applicant json
        missing_admitted_uins = admitted_uins - found_admitted_uins
        print(f"Missing UINs:\n {missing_admitted_uins}")
        
        # Save the updated data
        with open(output_file, 'w') as f:
            json.dump(updated_applicants, f, indent=4)
        
        print(f"Updated admission status for {len(found_admitted_uins)} out of {len(admitted_uins)} admitted UINs")
        print(f"Successfully processed {len(updated_applicants)} applicants")
        print(f"Updated data saved to {output_file}")
        
    except Exception as e:
        print(f"Error processing files: {e}")


def main():
    """
    Main function to run the update process
    """
    print("Update Applicant Admission Information")
    print("-" * 30)
    
    # Get file paths from user or use defaults
    applicants_file = input("Enter path to applicants JSON file (default: applicants.json): ") or "applicants.json"
    admitted_csv_file = input("Enter path to admitted UINs CSV file (default: admitted.csv): ") or "admitted.csv"
    output_file = input("Enter path for output JSON file (default: updated_applicants.json): ") or "updated_applicants.json"
    
    # Verify files exist
    files_exist = True
    for file_path in [applicants_file, admitted_csv_file]:
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} does not exist!")
            files_exist = False
    
    if files_exist:
        update_admission(applicants_file, admitted_csv_file, output_file)
    else:
        print("Please check file paths and try again.")


if __name__ == "__main__":
    main()