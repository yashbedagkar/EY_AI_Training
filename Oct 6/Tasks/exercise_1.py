import json
import logging

logging.basicConfig(
    filename="app1.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

students =[
{"name": "Rahul", "age": 21, "course": "AI", "marks": 85},
{"name": "Priya", "age": 22, "course": "ML", "marks": 90}]

with open("students.json", "w") as f:
    json.dump(students, f,indent =4)

logging.info("Added data created a json file")

with open("students.json", "r") as f:
    data = json.load(f)

for i in range(len(data)):
    print(data[i]["name"])

logging.info("Printed the names")

new_data = {"name": "Arjun", "age": 20, "course": "Data Science", "marks": 78}
data.append(new_data)

logging.info("Added new data")

with open("students.json", "w") as f:
    json.dump(data, f, indent=4)

logging.info("Updated the json file")


