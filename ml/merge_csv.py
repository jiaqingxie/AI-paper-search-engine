import pandas as pd
import os

base_df = pd.DataFrame()
clean_data_folder = "./Papers"

for filename in os.listdir(clean_data_folder):
    full_path1 = f"{clean_data_folder}/{filename}"
    for filename2 in os.listdir(full_path1):
        full_path = f"{clean_data_folder}/{filename}/{filename2}"
        print(full_path)

        # load data into a DataFrame
        new_df = pd.read_csv(full_path)

        # merge into the base DataFrame
        base_df = pd.concat([base_df, new_df])
        base_df.to_csv(f"./ml/papers.csv", index=False)