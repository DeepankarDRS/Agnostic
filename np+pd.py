
import numpy as np
import pandas as pd

# ------------------------------------------------------------
# 🔥 ADVANCED NUMPY
# ------------------------------------------------------------

# Broadcasting tricks: distance matrix
X = np.random.rand(5, 2)  # 5 points in 2D
dist = np.sqrt(((X[:, None, :] - X[None, :, :])**2).sum(axis=2))
print("\nDistance Matrix:\n", dist)

# Einstein Summation (einsum) – compact tensor operations
A = np.random.rand(3, 4)
B = np.random.rand(4, 5)
C = np.einsum("ik,kj->ij", A, B)  # same as A @ B
print("\nEinsum Matrix Multiply:\n", C)

# Memory views vs copy
arr = np.arange(10)
view = arr[::2]      # view, modifies original
view[:] = -1
print("\nMemory View:", arr)

# Stride tricks (create sliding windows without loops)
from numpy.lib.stride_tricks import sliding_window_view
sw = sliding_window_view(np.arange(10), window_shape=3)
print("\nSliding Windows:\n", sw)

# Masked arrays
masked = np.ma.masked_array([1, 2, -999, 4], mask=[0, 0, 1, 0])
print("\nMasked Mean:", masked.mean())

# Random advanced
np.random.seed(42)
print("\nMultivariate Normal:\n", np.random.multivariate_normal([0, 0], [[1, .5],[.5, 1]], 5))

# ------------------------------------------------------------
# 🔥 ADVANCED PANDAS
# ------------------------------------------------------------

# MultiIndex with slicing
arrays = [["A", "A", "B", "B"], [1, 2, 1, 2]]
multi_idx = pd.MultiIndex.from_arrays(arrays, names=("Letter", "Number"))
multi_df = pd.DataFrame({"Value": [10, 20, 30, 40]}, index=multi_idx)
print("\nMultiIndex DataFrame:\n", multi_df)
print("\nCross-section (Letter=A):\n", multi_df.xs("A"))

# Pivot with multiple aggregations
df = pd.DataFrame({
    "Region": ["East", "East", "West", "West"],
    "Product": ["A", "B", "A", "B"],
    "Sales": [100, 150, 200, 250],
    "Profit": [30, 50, 70, 90]
})
pivot = pd.pivot_table(df, values=["Sales", "Profit"], index="Region", aggfunc={"Sales": "sum", "Profit": "mean"})
print("\nPivot with Multiple Agg:\n", pivot)

# Window functions
ts = pd.Series(np.random.randn(10), index=pd.date_range("2025-01-01", periods=10))
print("\nRolling Mean:\n", ts.rolling(window=3).mean())
print("\nExpanding Max:\n", ts.expanding().max())

# Categorical optimization
df_cat = pd.DataFrame({"Grade": ["A", "B", "A", "C", "B"]})
df_cat["Grade"] = pd.Categorical(df_cat["Grade"], categories=["A", "B", "C"], ordered=True)
print("\nCategorical Codes:", df_cat["Grade"].cat.codes)

# Method chaining with pipe
df_chain = (df.assign(Margin=lambda x: x["Profit"]/x["Sales"])
              .query("Sales > 120")
              .groupby("Region")
              .agg({"Margin": "mean"}))
print("\nMethod Chaining:\n", df_chain)

# Query API with local variables
threshold = 180
print("\nQuery with local var:\n", df.query("Sales > @threshold"))

# Apply custom function row-wise
df["Perf"] = df.apply(lambda row: "High" if row["Profit"] > 60 else "Low", axis=1)
print("\nCustom Apply:\n", df)

# Efficient string methods
df_str = pd.Series(["  Hello ", "WORLD!!", "pandas_rocks"])
print("\nString Ops:\n", df_str.str.strip().str.lower().str.replace("!", "").str.contains("world"))

# Style formatting (Jupyter only)
# df.style.highlight_max(color="lightgreen").hide_index()

