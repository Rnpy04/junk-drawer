import pandas as pd

def merge_excel_files(output_file, *excel_files):
    all_data = []

    for file in excel_files:
        df = pd.read_excel(file)
        all_data.append(df)

    merged_df = pd.concat(all_data, ignore_index=True)
    merged_df.to_excel(output_file, index=False)

merge_excel_files(
    "merged.xlsx",
    "file1.xlsx",
    "file2.xlsx"
)
