# Pytest - API testing with Python `requests`

#### Pytest is a mature full-featured Python testing frame that helps you write and run tests in Python.

#### The `requests` module allows you to send HTTP requests using Python.

## Getting started

       
* To download and install `pytest`, run this command from the terminal : `python -m venv venv`
* source venv/bin/activate

To ensure all dependencies are resolved in a CI environment, in one go, add them to a `requirements.txt` file.
* Then run the following command : `pip install -r requirements.txt`

By default pytest only identifies the file names starting with `test_` or ending with `_test` as the test files.

Pytest requires the test method names to start with `test`. All other method names will be ignored even if we explicitly ask to run those methods.

A sample test below :

```python
def test_fetch_user() :
    path = "api/users/2"
    response = requests.get(url=baseUrl+path)
    responseJson = json.loads(response.text)
    assert respponse.status_code == 200
    assert jsonpath.jsonpath(responseJson,'$.data.first_name')[0] == 'Janet'
    assert jsonpath.jsonpath(responseJson,'$.data.id')[0] == 2

```
## Running tests
1. Create '.env' file with 'TOKEN={your_token}' and 'BASE_URL=https://api.clickup.com/api/v2'

2. Open the file 'Tests/test_space_methods.py' and replace the space id '90-------30' and the team id '90------72' by yours

3. If your tests are contained inside a folder 'Tests', then run the following command : `pytest Tests` 

To generate xml results, run the following command : `pytest Tests --junitxml="result.xml"`

pytest --html=report.html --self-contained-html
pytest --html=./report/report.html   