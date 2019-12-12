import pytest
import sys
import json

from jobs import app
from .utils import (
    template_data,
    template_exists,
    template_extends,
    inspect,
    get_functions,
    get_statements,
)


@pytest.mark.test_apply_template
def test_apply_template():
    assert template_exists(
        "apply"
    ), "The `apply.html` template does not exist in the `templates` folder."
    el = template_data("apply").select(".field.is-grouped .control .button.is-text")
    assert len(el) == 1
    assert "layout.html" in template_extends(
        "apply"
    ), "The `apply.html` template does not extend `layout.html`."


@pytest.mark.test_app_apply_route
def test_app_apply_route():
    assert "apply" in dir(app), "Create the `apply` function"
    assert (
        "job_id" in inspect.getfullargspec(app.apply).args
    ), "Add the correct parameters to the `apply` function parameter list"
    assert (
        "route:/jobs/<job_id>/apply:methods:[{'s': 'GET'}, {'s': 'POST'}]"
        or "route:/jobs/<job_id>/apply/<complete>:methods:[{'s': 'POST'}, {'s': 'GET'}]"
        in get_functions(app.apply)
    ), "Add a route decorator with the correct URL pattern and methods"


@pytest.mark.test_app_apply_post_request_check
def test_app_apply_post_request_check():
    assert "apply" in dir(app), "Create the `apply` function"
    assert "datetime" in dir(app), "`datetime` has not been imported."

    if_statement = get_statements(app.apply)[0]
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
    name = {
        "targets/id": "name",
        "value/slice/value/s": "name",
        "value/value/attr": "form",
        "value/value/value/id": "request",
    }
    cover_letter = {
        "targets/id": "cover_letter",
        "value/slice/value/s": "cover_letter",
        "value/value/attr": "form",
        "value/value/value/id": "request",
    }
    date = {
        "targets/id": "date",
        "value/args/s": "%m/%d/%Y",
        "value/func/attr": "strftime",
        "value/func/value/func/attr": "now",
        "value/func/value/func/value/attr": "datetime",
        "value/func/value/func/value/value/id": "datetime",
    }
    assert (
        post and method and request and eq
    ), 'Add an `if` statement to test if the request method equals "POST"'
    assert name in body, "Create the `name` variable"
    assert cover_letter in body, "Create the `cover_letter` variable"
    assert date in body, "Create the `date` variable"

