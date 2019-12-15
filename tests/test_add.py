import pytest
import sys
import json

from jobs import app
from .utils import (
    template_data,
    template_exists,
    template_extends,
    template_functions,
    inspect,
    get_functions,
    get_functions_returns,
    get_statements,
)


@pytest.mark.test_add_template
def test_add_template():
    assert template_exists(
        "add"
    ), "The `add.html` template does not exist in the `templates` folder."
    el = template_data("add").select(".field.is-grouped .control .button.is-text")
    assert len(el) == 1
    assert "layout.html" in template_extends(
        "add"
    ), "The `add.html` template does not extend `layout.html`."


@pytest.mark.test_app_add_route
def test_app_add_route():
    assert "add" in dir(app), "Create the `add` function"
    assert (
        "job_id" in inspect.getfullargspec(app.add).args
    ), "Add the correct parameters to the `add` function parameter list"
    assert (
        "route:/jobs/edit/<job_id>:methods:[{'s': 'GET'}, {'s': 'POST'}]"
        or "route:/jobs/add/:methods:[{'s': 'POST'}, {'s': 'GET'}]"
        in get_functions(app.add)
    ), "Add a route decorator with the correct URL pattern and methods"
    return_values = get_functions_returns(app.add)
    jobs = {
        "value/args/args/s": "jobs",
        "value/args/func/id": "url_for",
        "value/func/id": "redirect",
    }

    assert jobs in return_values, "Return a call to `redirect` and `url_for`"


@pytest.mark.test_app_add_post_request_check
def test_app_add_post_request_check():
    assert "add" in dir(app), "Create the `add` function"

    if_statement = get_statements(app.add)[1]
    body = if_statement["body"]
    post = (
        "test/comparators/s" in if_statement
        and "POST" == if_statement["test/comparators/s"]
    )
    method = (
        "test/left/attr" in if_statement and "method" == if_statement["test/left/attr"]
    )
    request = (
        "test/left/value/id" in if_statement
        and "request" == if_statement["test/left/value/id"]
    )
    eq = (
        "test/ops/node_type" in if_statement
        and "Eq" == if_statement["test/ops/node_type"]
    )
    title = {
        "targets/id": "title",
        "value/slice/value/s": "title",
        "value/value/attr": "form",
        "value/value/value/id": "request",
    }
    employer_id = {
        "targets/id": "employer_id",
        "value/slice/value/s": "employer",
        "value/value/attr": "form",
        "value/value/value/id": "request",
    }
    salary = {
        "targets/id": "salary",
        "value/slice/value/s": "salary",
        "value/value/attr": "form",
        "value/value/value/id": "request",
    }
    description = {
        "targets/id": "description",
        "value/slice/value/s": "description",
        "value/value/attr": "form",
        "value/value/value/id": "request",
    }

    assert (
        post and method and request and eq
    ), 'Add an `if` statement to test if the request method equals "POST"'

    assert employer_id in body, "Create the `employee_id` variable"
    assert salary in body, "Create the `rating` variable"
    assert title in body, "Create the `title` variable"
    assert description in body, "Create the `status` variable"


@pytest.mark.test_app_add_insert_job
def test_app_add_insert_job():
    assert "add" in dir(app), "Create the `add` function"
    execute_sql = "execute_sql:UPDATE job SET title=?, description=?, salary=?, employer_id=? WHERE id = ?:[{'id': 'title'}, {'id': 'description'}, {'id': 'salary'}, {'id': 'employer_id'}, {'id': 'job_id'}]:commit:True"

    print(get_functions(app.add))

    assert execute_sql in get_functions(
        app.add
    ), "`execute_sql` for update has not been called or has the wrong parameters."

    execute_sql = "execute_sql:INSERT INTO job (title, description, salary, employer_id) VALUES (?, ?, ?, ?):[{'id': 'title'}, {'id': 'description'}, {'id': 'salary'}, {'id': 'employer_id'}]:commit:True"
    assert execute_sql in get_functions(
        app.add
    ), "`execute_sql` for insert has not been called or has the wrong parameters."


@pytest.mark.test_app_redirect_to_jobs
def test_app_redirect_to_jobs():
    assert "add" in dir(app), "Create the `add` function"
    assert "redirect" in dir(app), "`redirect` has not been imported from flask."
    assert "url_for" in dir(app), "`url_for` has not been imported from flask."
    assert "redirect:jobs:url_for" in get_functions(
        app.add
    ), "redirect back to the jobs page"
