import pytest
import requests
from config import BASE_URL


@pytest.fixture
def base_url():
    return BASE_URL


def test_Employee_lifecycle(base_url):
    payload = {"name": "Master Samir", "Role": "Automation"}
    requests.post(base_url, json=payload, timeout=5)

    response_get = requests.get(base_url, timeout=5)
    data = response_get.json()
    assert data['Employee_details']['name'] == "Master Samir"
    assert data['Employee_details']['Role'] == "Automation"
    print("Lifecycle test passed: Created and Verified!")


def test_create_Employee_invalid_name(base_url):
    bad_payload = {"name": "A", "Role": "Hacking"}
    response = requests.post(base_url, json=bad_payload, timeout=5)
    assert response.status_code == 400
    assert "error" in response.json()


def test_full_Employee_lifecycle(base_url):
    new_emp = {"name": "Engineer Samir", "Role": "QA Expert"}
    requests.post(base_url, json=new_emp, timeout=5)
    delete_url = f"{base_url}/Engineer Samir"
    response = requests.delete(delete_url, timeout=5)
    assert response.status_code == 200
    assert response.json()['status'] == "success"
