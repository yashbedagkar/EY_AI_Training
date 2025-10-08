from fastapi.testclient import TestClient
from courses_api import app
import pytest

client = TestClient(app)

def test_course_creation():
    new_course ={"id": 2,
                 "title": "ML Basics",
                 "duration": 40,
                 "fee": 3500,
                 "is_active":True}
    response = client.post("/courses",json=new_course)
    assert response.status_code == 201
    assert response.json() == new_course

@pytest.mark.parametrize("duplicate_course", [
    {"id": 1,
     "title": "Python Basics",
     "duration": 30,
     "fee": 3000,
     "is_active":True},
    {"id": 2,
     "title": "ML Basics",
     "duration": 40,
     "fee": 3500,
     "is_active": True}
])

def test_duplicate_course_creation(duplicate_course):
    response = client.post("/courses", json=duplicate_course)
    assert response.status_code == 400
    assert response.json()["detail"] == "Course ID already exists"

def test_validation_error_on_invalid_course_data():
    invalid_course = {
        "id": 2,
        "title": "AI",
        "duration": 0,   # Invalid: must be > 0
        "fee": -500,     # Invalid: must be > 0
        "is_active": True
    }
    response = client.post("/courses", json=invalid_course)
    assert response.status_code == 422
    response_text = response.text
    assert "Input should be greater than 0" in response.text

def test_check_fields_and_types():
    response = client.get("/courses")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert all("id" in course for course in data)
    assert all("title" in course for course in data)
    assert all("duration" in course for course in data)
    assert all("fee" in course for course in data)
    assert all("is_active" in course for course in data)