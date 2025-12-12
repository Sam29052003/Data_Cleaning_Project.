
import numpy as np

arr = np.array([10, 20, 30, 40])
print(arr * 2)
print(arr.mean())


import pandas as pd

data = {
    "Name": ["Sam", "Riya", "Arjun"],
    "Marks": [85, 92, 78],
    "City": ["Mumbai", "Delhi", "Pune"]
}

df = pd.DataFrame(data)

print(df)
print("\nSummary:")
print(df.describe())
