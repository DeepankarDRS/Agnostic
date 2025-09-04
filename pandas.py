# ============================================================
# Pandas Complete Cheatsheet (Basic → Advanced)
# Copy & Paste into a Python file / Jupyter Notebook
# ============================================================

import pandas as pd
import numpy as np

# ------------------------------------------------------------
# 1. Creating Series and DataFrame
# ------------------------------------------------------------
s = pd.Series([10, 20, 30], index=["a", "b", "c"])
print("\nSeries:\n", s)

data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Salary": [50000, 60000, 70000]
}
df = pd.DataFrame(data)
print("\nDataFrame:\n", df)

# ------------------------------------------------------------
# 2. Importing / Exporting Data
# ------------------------------------------------------------
# df = pd.read_csv("file.csv")
# df.to_csv("out.csv", index=False)

# ------------------------------------------------------------
# 3. Exploring Data
# ------------------------------------------------------------
print(df.head())       # first 5 rows
print(df.tail())       # last 5 rows
print(df.info())       # summary
print(df.describe())   # stats for numeric columns
print(df.shape)        # (rows, columns)
print(df.columns)      # column names

# ------------------------------------------------------------
# 4. Selecting & Indexing
# ------------------------------------------------------------
print(df["Name"])             # select single column
print(df[["Name", "Age"]])    # multiple columns
print(df.iloc[0])             # row by position
print(df.loc[0])              # row by label
print(df.iloc[0:2])           # slicing
print(df.loc[:, "Age"])       # all rows, Age column
print(df[df["Age"] > 28])     # filtering

# ------------------------------------------------------------
# 5. Adding / Modifying Columns
# ------------------------------------------------------------
df["Bonus"] = df["Salary"] * 0.1
df["Senior"] = df["Age"] > 28
print("\nModified DataFrame:\n", df)

# ------------------------------------------------------------
# 6. Removing Data
# ------------------------------------------------------------
df2 = df.drop("Bonus", axis=1)        # drop column
df3 = df.drop(1, axis=0)              # drop row by index
print("\nAfter Drop:\n", df2)

# ------------------------------------------------------------
# 7. Sorting
# ------------------------------------------------------------
print(df.sort_values("Salary"))       # ascending
print(df.sort_values("Salary", ascending=False))  # descending

# ------------------------------------------------------------
# 8. Aggregation & Statistics
# ------------------------------------------------------------
print(df["Salary"].mean())
print(df["Salary"].sum())
print(df["Age"].min(), df["Age"].max())

# ------------------------------------------------------------
# 9. GroupBy
# ------------------------------------------------------------
print("\nGroupBy Example:")
group = df.groupby("Senior")["Salary"].mean()
print(group)

# ------------------------------------------------------------
# 10. Handling Missing Values
# ------------------------------------------------------------
df_nan = pd.DataFrame({
    "A": [1, 2, np.nan, 4],
    "B": ["x", np.nan, "y", "z"]
})
print("\nMissing Values:\n", df_nan)
print(df_nan.isnull().sum())
df_filled = df_nan.fillna({"A": 0, "B": "missing"})
print("\nAfter Fillna:\n", df_filled)
df_dropped = df_nan.dropna()
print("\nAfter Dropna:\n", df_dropped)

# ------------------------------------------------------------
# 11. Merge, Join, Concat
# ------------------------------------------------------------
df1 = pd.DataFrame({"ID": [1, 2], "Name": ["Alice", "Bob"]})
df2 = pd.DataFrame({"ID": [1, 2], "Salary": [50000, 60000]})
merged = pd.merge(df1, df2, on="ID")
print("\nMerged:\n", merged)

concat = pd.concat([df1, df2], axis=1)
print("\nConcatenated:\n", concat)

# ------------------------------------------------------------
# 12. Pivot Tables & Crosstab
# ------------------------------------------------------------
df_sales = pd.DataFrame({
    "Region": ["East", "West", "East", "West"],
    "Product": ["A", "A", "B", "B"],
    "Sales": [100, 200, 150, 250]
})
pivot = pd.pivot_table(df_sales, values="Sales", index="Region", columns="Product", aggfunc="sum")
print("\nPivot Table:\n", pivot)

cross = pd.crosstab(df_sales["Region"], df_sales["Product"])
print("\nCrosstab:\n", cross)

# ------------------------------------------------------------
# 13. Applying Functions
# ------------------------------------------------------------
df["Salary_Lakh"] = df["Salary"].apply(lambda x: x/100000)
print("\nApply:\n", df)

# ------------------------------------------------------------
# 14. Advanced Indexing (MultiIndex)
# ------------------------------------------------------------
arrays = [["A", "A", "B", "B"], [1, 2, 1, 2]]
multi_idx = pd.MultiIndex.from_arrays(arrays, names=("Letter", "Number"))
multi_df = pd.DataFrame({"Value": [10, 20, 30, 40]}, index=multi_idx)
print("\nMultiIndex DF:\n", multi_df)

# ------------------------------------------------------------
# 15. Time Series
# ------------------------------------------------------------
dates = pd.date_range("2025-01-01", periods=5, freq="D")
ts = pd.Series(np.random.randn(5), index=dates)
print("\nTime Series:\n", ts)
print(ts.resample("2D").mean())

# ------------------------------------------------------------
# 16. Window Functions (Rolling, Expanding)
# ------------------------------------------------------------
print("\nRolling Mean:\n", ts.rolling(window=2).mean())
print("\nExpanding Sum:\n", ts.expanding().sum())

# ------------------------------------------------------------
# 17. Advanced: Categoricals
# ------------------------------------------------------------
df_cat = pd.DataFrame({"Category": ["Low", "Medium", "High", "Low"]})
df_cat["Category"] = pd.Categorical(df_cat["Category"], categories=["Low", "Medium", "High"], ordered=True)
print("\nCategoricals:\n", df_cat)

# ------------------------------------------------------------
# 18. Advanced: String Operations
# ------------------------------------------------------------
df_str = pd.DataFrame({"Text": ["  hello ", "WORLD", "pandas rocks!"]})
print("\nString Ops:\n", df_str["Text"].str.strip().str.lower().str.replace("!", ""))

# ------------------------------------------------------------
# 19. Advanced: Query API
# ------------------------------------------------------------
print("\nQuery API:\n", df.query("Age > 28 & Salary > 55000"))

# ------------------------------------------------------------
# 20. Advanced: Styling (Jupyter only)
# ------------------------------------------------------------
# df.style.highlight_max(color="yellow").hide_index()

# ============================================================
# END OF CHEATSHEET
# ============================================================
