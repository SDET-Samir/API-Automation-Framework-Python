![CI Status](https://github.com)

# API Automation Testing Framework
A robust, scalable automation suite designed to ensure the reliability of Employee Management APIs. This framework follows the **Data-Driven Testing** pattern and is fully integrated with **CI/CD pipelines**.

## Tech Stack
- **Language:** Python
- **Library:** Requests (API interaction)
- **Framework:** Pytest (Test management)
- **Reporting:** Pytest-HTML (Visual reports)

## Scenarios Covered
1. **End-to-End Lifecycle:** Creating a student via POST and verifying data integrity via GET.
2. **Security/Negative Testing:** Validating server response (400 Bad Request) against invalid data.

## How to Generate Reports
Run the following command:
`pytest --html=report.html`

## Business Value & Test Coverage
This framework ensures the stability of the Employee Management System by covering critical business flows:

- **Data Integrity Validation (GET/POST):** Ensures that every employee record created is stored accurately without data corruption.
- **Security & Input Validation:** Protects the database by rejecting malformed requests (e.g., empty names or invalid roles), preventing system crashes.
- **Regression Assurance (DELETE):** Guarantees that the removal of records is permanent and doesn't leave "ghost data" in the system, maintaining database hygiene.
- **Error Resilience:** Validates that the API correctly handles non-existent resources (404) and server-side issues (500), ensuring a smooth user experience.

## Project Structure
- `server.py`: The Mock Flask Server.
- `tests/`: Contains automated test cases.
- `config.py`: Configuration settings for different environments.
- `requirements.txt`: Project dependencies.

## Sample Report
Once you run the tests, open `report.html` to see the visual execution results..

