from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age : int
    email : str
    is_active : bool = True

data = {
    "name": "Aisha",
    "age": 21,
    "email": "aisha@example.com",
}

student=Student(**data)
print(student)
print(student.name)

# invalid_data = {"name": "Rahul", "age": "twenty", "email": "rahul@example.com"}
# student = Student(**invalid_data)