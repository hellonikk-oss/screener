import openpyxl
import openpyxl
import pandas as pd
import os


df1 = pd.read_excel('./cmhelpline/cmhelpline_L2.xls', sheet_name='Data')
df2 = pd.read_excel('./cmhelpline/cmhelpline_L3.xls', sheet_name='Data')
df3 = pd.read_excel('./cmhelpline/cmhelpline_L4.xls', sheet_name='Data')
df = pd.concat([df1,df2,df3], ignore_index=True)
df.to_excel('./cmhelpline/high_level.xlsx', index=False)
source_wb = openpyxl.load_workbook('./cmhelpline/high_level.xlsx')
dest_wb =openpyxl.load_workbook('./cmhelpline/final_high_level.xlsx')
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
dest_wb.save('./cmhelpline/final_high_level.xlsx')
    
        # 7. Close workbooks to free memory
source_wb.close()
dest_wb.close()
        
print("Old data cleared safely, and new data successfully copied!")
