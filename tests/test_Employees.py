from utils import load_test_data
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


def test_employee_lifecycle(base_url):
    new_emp = {"name": "Ahmad Samir", "Major": "software QA"}
    response_post = requests.post(base_url, json=new_emp)
    res_json = response_post.json()

    assert response_post.status_code == 201
    assert "Employee_details" in res_json

    delete_url = f"{base_url}/Ahmad Samir"
    res_delete = requests.delete(delete_url)
    assert res_delete.status_code == 200
    res_verify = requests.get(base_url)
    assert res_verify.json()["Employee_details"]["name"]
    logger.info("verified: Employee is actually gone from DB ")


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


def test_delete_non_exixtent_employee(base_url):
    fake_name = "Ghost_User_99"
    delete_url = f"{base_url}/{fake_name}"
    response = requests.delete(delete_url, timeout=5)
    assert response.status_code == 404
    logger.info(f"correctly handled deletion of non-existent user:{fake_name}")
