import pandas as pd

data = {
    "Name": ["Rahul", "Priya", "Arjun", "Neha", "Vikram"],
    "Age": [21, 22, 20, 23, 21],
    "Course": ["AI", "ML", "Data Science", "AI", "ML"],
    "Marks": [85, 90, 78, 88, 95]
}

df= pd.DataFrame(data)

print(df["Name"])
print(df[["Name","Age"]])
print(df.iloc[0])
print(df.loc[2,"Course"])