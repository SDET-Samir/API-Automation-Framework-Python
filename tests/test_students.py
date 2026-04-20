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
    print("✅ Lifecycle test passed: Created and Verified!")
