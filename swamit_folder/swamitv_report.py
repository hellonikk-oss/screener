import io
import os
import openpyxl

# 1. Define the paths to your files
folder_name = 'cmhelpline'
file1_path = os.path.join(folder_name, 'swamitv_report.xlsx')

def get_source_file_path():
    # Prefer swamitv.xlsx, fallback to swamitv.xls
    candidates = ['swamitv.xlsx', 'swamitv.xls']
    for filename in candidates:
        path = os.path.join(folder_name, filename)
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        f"Could not find {' or '.join(candidates)} in '{folder_name}'."
    )

def load_source_rows(source_path):
    with open(source_path, 'rb') as f:
        content = f.read()

    # Check if file has OOXML / zip header
    if content.startswith(b'PK\x03\x04'):
        src_wb = openpyxl.load_workbook(io.BytesIO(content), data_only=True)
        src_sheet = src_wb.active
        return list(src_sheet.iter_rows(values_only=True))
    else:
        # Fallback to pandas for legacy binary .xls or HTML
        import pandas as pd
        df = pd.read_excel(source_path)
        rows = [list(df.columns)]
        for row in df.itertuples(index=False):
            rows.append(list(row))
        return rows

def copy_excel_data():
    try:
        source_path = get_source_file_path()

        # 2. Load target Excel workbook
        print(f"Loading {file1_path}...")
        wb1 = openpyxl.load_workbook(file1_path)
        
        print(f"Loading source data from {source_path}...")
        source_rows = load_source_rows(source_path)
        
        # 3. Access "Sheet2" in target workbook (or create it if it doesn't exist)
        target_sheet_name = 'Sheet2'
        if target_sheet_name in wb1.sheetnames:
            target_sheet = wb1[target_sheet_name]
        else:
            target_sheet = wb1.create_sheet(title=target_sheet_name)
            
        print(f"Copying data to {target_sheet_name} starting at A1...")
        
        old_max_row = target_sheet.max_row or 0
        old_max_col = target_sheet.max_column or 0

        # 4. Write data to Sheet2
        for row_idx, row in enumerate(source_rows, start=1):
            for col_idx, value in enumerate(row, start=1):
                target_sheet.cell(row=row_idx, column=col_idx, value=value)

        # 5. Clear excess cells if the new data is smaller than existing sheet
        new_max_row = len(source_rows)
        new_max_col = max((len(r) for r in source_rows), default=0)

        if old_max_row > new_max_row:
            for r in range(new_max_row + 1, old_max_row + 1):
                for c in range(1, max(old_max_col, new_max_col) + 1):
                    target_sheet.cell(row=r, column=c, value=None)

        if old_max_col > new_max_col:
            for r in range(1, new_max_row + 1):
                for c in range(new_max_col + 1, old_max_col + 1):
                    target_sheet.cell(row=r, column=c, value=None)
                
        # 6. Save the changes made to target file
        wb1.save(file1_path)
        print("Data successfully copied and saved to swamitv_report.xlsx!")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the function
if __name__ == "__main__":
    copy_excel_data()
