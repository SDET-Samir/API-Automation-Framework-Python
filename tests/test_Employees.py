import logging
import pytest
import requests
from config import BASE_URL


@pytest.fixture
def base_url():
    return BASE_URL


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_Employee_lifecycle(base_url):
    payload = {"name": "Master Samir", "Role": "Automation"}
    logger.info(f"Step 1: Creating employee with payload: {payload}")
    response_post = requests.post(base_url, json=payload, timeout=5)
    assert response_post.status_code == 201

    logger.info("Step 2: Fetching employee data from server")
    response_get = requests.get(base_url, timeout=5)
    data = response_get.json()
    logger.info(
        f"Step 3: Verifying data. Found name: {data['Employee_details']['name']}")

    assert data['Employee_details']['name'] == "Master Samir"
    assert data['Employee_details']['Role'] == "Automation"

    logger.info("Lifecycle test completed successfully!")


@pytest.mark.parametrize("bad_name", ["A", "Ab", "", "  "])
def test_create_employee_invalid_names(base_url, bad_name):
    payload = {"name": bad_name, "Role": "QA"}
    response = requests.post(base_url, json=payload, timeout=5)
    assert response.status_code == 400
    logger.info(f"Successfully rejected invalid name: {bad_name}")


def test_full_Employee_lifecycle(base_url):
    new_emp = {"name": "Engineer Samir", "Role": "QA Expert"}
    requests.post(base_url, json=new_emp, timeout=5)
    delete_url = f"{base_url}/Engineer Samir"
    response = requests.delete(delete_url, timeout=5)
    assert response.status_code == 200
    assert response.json()['status'] == "success"


@pytest.mark.parametrize("null_name", ["", "...", "  "])
def test_create_employee_null_names(base_url, null_name):
    payload = {"name": null_name, "Role": "QA"}
    response = requests.post(base_url, json=payload, timeout=5)
    assert response.status_code == 400
    logger.info(f"Successfully rejected invalid name: {null_name}")
