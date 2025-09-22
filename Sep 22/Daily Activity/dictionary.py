student = {
    "name": "Yash",
    "age" : "22",
    "city" : "Pune"
}

# accessing a dictionary
print(student["name"])
print(student.get("age"))

student["course"]="AI" #adding a key-value pair
student["city"] = "BLR" #updating existing key

print(student)

student.pop("city") #removing key
del student["course"] #deleting key

print(student)