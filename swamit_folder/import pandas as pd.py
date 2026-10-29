import pandas as pd
import os

# 1. Define the updated paths to your files
# Replace 'my_folder' with the actual name of your project subdirectory
folder_name = 'cmhelpline'
file1_path = os.path.join(folder_name, 'swamitv_report.xlsx')
file2_path = os.path.join(folder_name, 'swamitv.xls')

def copy_excel_data():
    try:
        print(f"Reading data from {file2_path}...")
        # 2. Read the older .xls format into a Pandas DataFrame
        df = pd.read_excel(file2_path)
        
        print(f"Writing data to {file1_path} (Sheet2, cell A1)...")
        # 3. Write to the .xlsx file using the openpyxl engine
        # mode='a' (append) ensures we don't delete existing sheets in swamitv_report.xlsx
        # if_sheet_exists='replace' creates or overwrites only 'Sheet2'
        with pd.ExcelWriter(file1_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name='Sheet2', index=False, startrow=0, startcol=0)
            
        print("Data successfully copied and saved to swamitv_report.xlsx!")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find the file. Please check your subdirectory and file names. Details: {e}")
    except ValueError as e:
        # Handles the case where swamitv_report.xlsx doesn't exist yet to append to
        print(f"Error: The target file {file1_path} must already exist to append a new sheet. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    copy_excel_data()