from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

class Employee(BaseModel):
    id:int
    name: str
    department: str
    salary : float

employees =[
    {"id":1,"name":"Amit Sharma","department":"HR","salary":50000}
]

@app.get("/employees")
def get_all():
    return employees

@app.post(path="/employees",status_code=201)
def add_employee(employee: Employee):
    employees.append(employee.dict())
    return employee

@app.get("/employees/{emp_id}")
def get_employee(emp_id:int):
    for e in employees:
        if e["id"] == emp_id:
            return e
    raise HTTPException(status_code=404, detail="Employee not found")

@app.put("/employees/{emp_id}")
def update_employee(emp_id:int,updated_employee:Employee):
    for i, e in enumerate(employees):
        if e["id"] == emp_id:
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