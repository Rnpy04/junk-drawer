import pandas as pd

def merge_csv_files(output_file, *csv_files):
    df_list = [pd.read_csv(file) for file in csv_files]
    merged_df = pd.concat(df_list, ignore_index=True)
    merged_df.to_csv(output_file, index=False)

merge_csv_files(
    "merged.csv",
    "data1.csv",
    "data2.csv",
    "data3.csv"
)
