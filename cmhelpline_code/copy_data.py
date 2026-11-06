
import openpyxl
import pandas as pd
import os

old_file_path = './cmhelpline/cmhelpline_1.xls' 
new_file_path = './cmhelpline/cmhelpline_1.xlsx'

if not os.path.exists(old_file_path):
    print(f"Error: Could not find the file at {old_file_path}")
else:
    # 1. Read the old .xls file and convert to .xlsx
    df = pd.read_excel(old_file_path)
    df.to_excel(new_file_path, index=False)

    # 2. Load the workbooks
    source_wb = openpyxl.load_workbook(new_file_path)
    dest_wb = openpyxl.load_workbook('./cmhelpline/L-1.xlsx')

    # 3. Select the source worksheet
    source_sheet = source_wb.active 

    # 4. CLEAR THE DATA ONLY (Keep the sheet intact to preserve references)
    if 'data_cmhl' in dest_wb.sheetnames:
        dest_sheet = dest_wb['data_cmhl']
        # This deletes all data from row 1 down to the very last row used
        if dest_sheet.max_row > 0:
            dest_sheet.delete_rows(1, dest_sheet.max_row)
    else:
        dest_sheet = dest_wb.create_sheet('data_cmhl')

    # 5. Iterate through the source data and copy it starting at A1
    for row_idx, row_data in enumerate(source_sheet.iter_rows(values_only=True), start=1):
        for col_idx, cell_value in enumerate(row_data, start=1):
            dest_sheet.cell(row=row_idx, column=col_idx, value=cell_value)

    # 6. Save the changes
    dest_wb.save('./cmhelpline/L-1.xlsx')

    # 7. Close workbooks to free memory
    source_wb.close()
    dest_wb.close()
    
    print("Old data cleared safely, and new data successfully copied!")