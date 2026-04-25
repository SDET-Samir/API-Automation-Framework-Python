# API Automation Testing Framework
A professional automated testing suite for Employee Management Systems.

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

## Test Coverage
1. **Get**
2. **Post**
3. **Delete**

## Project Structure
- `server.py`: The Mock Flask Server.
- `tests/`: Contains automated test cases.
- `config.py`: Configuration settings for different environments.
- `requirements.txt`: Project dependencies.

## Sample Report
Once you run the tests, open `report.html` to see the visual execution results..

