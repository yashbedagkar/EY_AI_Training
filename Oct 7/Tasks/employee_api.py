from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

class Employee(BaseModel):
    id:int
    name: str
    department: str
    salary : float

employees =[
    {"id":1,"name":"Rahul","department":"HR","salary":40000.0},
    {"id":2,"name":"Priya","department":"Consulting","salary":70000.0},
    {"id":3,"name":"Rohan","department":"Tax", "salary":60000.0}
]

#------------------GET------------------
@app.get("/employees")
def get_all_employees():
    return {"employees": employees}

@app.get("/employees/count")
def get_count_employees():
    return {"count": len(employees)}


@app.get("/employees/{employee_id}")
def get_employee(employee_id:int):
    for e in employees:
        if e["id"] == employee_id:
            return e
    raise HTTPException(status_code=404, detail="employee not found")


@app.post(path="/employees",status_code=201)
def add_employee(employee: Employee):
    for emp in employees:
        if emp["id"] == employee.id:
            return{"message":"employee already exists"}
        employees.append(employee.dict())
    return {"message":"Employee added successfully","employee":employee}

@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, updated_employee : Employee):
    for i, e in enumerate(employees):
        if e["id"] == employee_id:
            employees[i] = updated_employee.dict()
            return {"message":"Employee updated","employee":updated_employee}
    raise HTTPException(status_code=404, detail="Employee not found")

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    for i, e in enumerate(employees):
        if e["id"] == employee_id:
            del employees[i]
            return {"message": "Employee deleted successfully", "employee":e}
    raise HTTPException(status_code=404, detail="Employee not found")