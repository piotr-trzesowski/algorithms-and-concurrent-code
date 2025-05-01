from functools import reduce

import pandas as pd


# Example DataFrames
df1 = pd.DataFrame({"db": ["db1", "db2", "db3"], "table": ["table1", "table2", "table3"], "sum": [100, 200, 300]})

df2 = pd.DataFrame({"db": ["db1", "db2", "db4"], "table": ["table1", "table2", "table4"], "null": [10, 20, 40]})

# Merge on columns "db" and "table"
merged_df = pd.merge(df1, df2, on=["db", "table"], how="outer")

print(merged_df)

df3 = pd.DataFrame(
    {
        "db": ["db1", "db2", "db3"],
        "table": ["table1", "table2", "table3"],
        "column": ["col1", "col2", "col3"],
        "value1": [1, 2, 3],
    }
)

df4 = pd.DataFrame(
    {
        "db": ["db1", "db2", "db3"],
        "table": ["table1", "table2", "table3"],
        "column": ["col1", "col2", "col3"],
        "value2": [4, 5, 6],
    }
)

df5 = pd.DataFrame(
    {
        "db": ["db1", "db2", "db3"],
        "table": ["table1", "table2", "table3"],
        "column": ["col1", "col2", "col3"],
        "value3": [7, 8, 9],
    }
)

# List of DataFrames
dfs = [df3, df4, df5]

# Merge all DataFrames
merged_df = reduce(lambda left, right: pd.merge(left, right, on=["db", "table", "column"], suffixes=("", "_drop")), dfs)

# Drop any columns that end with '_drop'
merged_df = merged_df[[col for col in merged_df.columns if not col.endswith("_drop")]]

# This approach is more scalable if you have a large number of DataFrames to merge
print(merged_df)
