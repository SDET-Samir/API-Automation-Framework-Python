import pytest
import requests


@pytest.fixture
def base_url():
    return "http://localhost:5000/api/students"


def test_student_lifecycle(base_url):
    payload = {"name": "Master Samir", "major": "Automation"}
    requests.post(base_url, json=payload, timeout=5)

    response_get = requests.get(base_url, timeout=5)
    data = response_get.json()
    assert data['student_details']['name'] == "Master Samir"
    assert data['student_details']['major'] == "Automation"
    print("Lifecycle test passed: Created and Verified!")


def test_create_student_invalid_name(base_url):
    bad_payload = {"name": "A", "major": "Hacking"}
    response = requests.post(base_url, json=bad_payload)
    assert response.status_code == 400
    assert "error" in response.json()


def test_full_employee_lifecycle(base_url):
    new_emp = {"name": "Engineer Samir", "role": "QA Expert"}
    requests.post(base_url, json=new_emp, timeout=5)
    delete_url = f"{base_url}/Engineer Samir"
    response = requests.delete(delete_url, timeout=5)
    assert response.status_code == 200
    assert response.json()['status'] == "success"
