import json

student = {
    "name" : "Rahul",
    "age" : 21,
    "courses" : ["AI","ML"],
    "marks" :{"AI":85,"ML":90}
}

with open("student.json", "w") as f:
    json.dump(student, f,indent =4)

with open("student.json", "r") as f:
    data = json.load(f)

print(data["name"])
print(data["marks"]["AI"])
print(type(data))