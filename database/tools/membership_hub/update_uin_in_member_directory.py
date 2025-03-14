import json
import pandas as pd

def add_uin_to_member_directory(app_json, md):
    with open(app_json, 'r', encoding='utf-8') as f:
        app_data = json.load(f)

    for item in app_data:
        #get admitted applicant's name and uin
        if item['Admission'] == True:
            name = item['Name']
            uin = str(item['UIN'])

            print(f"Got admission data of {name} - {uin}")

            md.loc[md['Full Name'] == name, 'uin'] = uin
    return md

def main():
    app_file_dir = "../../data/app/"
    app_files = [
        "Spring_2025_NM_App.json",
        "Spring_2024_NM_App.json",
        "Spring_2023_NM_App.json",
        "Spring_2022_NM_App.json",
        "Fall_2024_NM_App.json",
        "Fall_2023_NM_App.json",
        "Fall_2022_NM_App.json",
    ]

    member_directory = "../../data/member_directory_original.csv"

    md = pd.read_csv(member_directory, dtype={'uin':str})

    #create uin column if it doesn't exist
    if 'uin' not in md.columns:
        md['uin'] = 'N/A'
    md['uin'] = md['uin'].astype(str)

    for app in app_files:
        app_file = app_file_dir + app
        print(f"Processing {app_file}")
        md = add_uin_to_member_directory(app_file, md)
        print(f"Process complete for {app_file}")

    md.to_csv("../../data/member_directory_updated_uin.csv", index=False)

if __name__ == "__main__":
    main()