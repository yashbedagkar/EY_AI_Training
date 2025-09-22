import pandas as pd

data = {
    "Name":["Yash", "Rahul","John", "Kim"],
    "Age":[22,24,52,63],
    "Course":["Python", "Science", "ML","Python"],
    "Marks": [45,76,23,57]
}

df=pd.DataFrame(data)
print(df)