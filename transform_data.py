import pandas as pd

# Step 1: Load the CSV file
df = pd.read_csv("employees.csv")
print("---- Original Data ----")
print(df, "\n")

# Step 2: FILTER rows (Example: employees with sales > 45,000)
filtered_df = df[df["sales"] > 45000]
print("---- Filter: Sales > 45000 ----")
print(filtered_df, "\n")

# Step 3: SORT data (Example: sort by sales in descending order)
sorted_df = df.sort_values(by="sales", ascending=False)
print("---- Sorted by Sales (High to Low) ----")
print(sorted_df, "\n")

# Step 4: AGGREGATE (Example: average sales per department)
agg_df = df.groupby("department")["sales"].mean().reset_index()
print("---- Average Sales by Department ----")
print(agg_df, "\n")

# Step 5: TOP PERFORMER
top_performer = df.loc[df["sales"].idxmax()]
print("---- Top Performer ----")
print(top_performer, "\n")
