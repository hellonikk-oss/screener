import pandas as pd
import os
import openpyxl

def download_Final_cmhelpline():
    # Base directory relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    cmhelpline_dir = os.path.join(project_dir, 'cmhelpline')

    final_file = os.path.join(cmhelpline_dir, 'final_high_level.xlsx')
    l1_file = os.path.join(cmhelpline_dir, 'L-1.xlsx')

    # Check if the file exists before trying to remove it
    if os.path.exists(final_file):
        os.remove(final_file)

    df1 = pd.read_excel(os.path.join(cmhelpline_dir, 'cmhelpline_L2.xls'), sheet_name='Data')
    df2 = pd.read_excel(os.path.join(cmhelpline_dir, 'cmhelpline_L3.xls'), sheet_name='Data')
    df3 = pd.read_excel(os.path.join(cmhelpline_dir, 'cmhelpline_L4.xls'), sheet_name='Data')
    df = pd.concat([df1, df2, df3], ignore_index=True)
    df.to_excel(final_file, index=False)

    source_wb = openpyxl.load_workbook(final_file)
    dest_wb = openpyxl.load_workbook(l1_file)
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
    
    # 6. Close source workbook before overwriting
    source_wb.close()

    # 7. Save the changes and close
    dest_wb.save(final_file)
    dest_wb.close()
        
    print("Old data cleared safely, and new data successfully copied!")

if __name__ == '__main__':
    download_Final_cmhelpline()
