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


@pytest.mark.test_login_template
def test_login_template():
    assert template_exists(
        "login"
    ), "The `login.html` template does not exist in the `templates` folder."
    el = template_data("login").select(".field .button.is-success")
    assert len(el) == 1
    assert "layout.html" in template_extends(
        "login"
    ), "The `login.html` template does not extend `layout.html`."


@pytest.mark.test_app_login_route
def test_app_login_route():
    assert "login" in dir(app), "Create the `login` function"
    assert (
        "route:/login:methods:[{'s': 'GET'}, {'s': 'POST'}]"
        or "route:/login:methods:[{'s': 'POST'}, {'s': 'GET'}]"
        in get_functions(app.login)
    ), "Add a route decorator with the correct URL pattern and methods"
    return_values = get_functions_returns(app.login)
    jobs = {
        "value/args/args/s": "jobs",
        "value/args/func/id": "url_for",
        "value/func/id": "redirect",
    }

    assert jobs in return_values, "Return a call to `redirect` and `url_for`"

@pytest.mark.test_app_logout_route
def test_app_logout_route():
    assert "logout" in dir(app), "Create the `logout` function"
    assert (
        "route:/logout"
        in get_functions(app.logout)
    ), "Add a route decorator with the correct URL pattern and methods"
    return_values = get_functions_returns(app.logout)
    jobs = {
        "value/args/args/s": "jobs",
        "value/args/func/id": "url_for",
        "value/func/id": "redirect",
    }

    assert jobs in return_values, "Return a call to `redirect` and `url_for`"


@pytest.mark.test_app_login_post_request_check
def test_app_login_post_request_check():
    assert "login" in dir(app), "Create the `login` function"

    if_statement = get_statements(app.login)[0]
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
    email = {
        "targets/id": "email",
        "value/slice/value/s": "email",
        "value/value/attr": "form",
        "value/value/value/id": "request",
    }
    password = {
        "targets/id": "password",
        "value/slice/value/s": "password",
        "value/value/attr": "form",
        "value/value/value/id": "request",
    }
    
    assert (
        post and method and request and eq
    ), 'Add an `if` statement to test if the request method equals "POST"'
            
    assert email in body, "Create the `email` variable"
    assert password in body, "Create the `password` variable"


@pytest.mark.test_login_redirect_to_jobs
def test_login_redirect_to_jobs():
    assert "login" in dir(app), "Create the `login` function"
    assert "redirect" in dir(app), "`redirect` has not been imported from flask."
    assert "url_for" in dir(app), "`url_for` has not been imported from flask."
    assert "redirect:jobs:url_for" in get_functions(
        app.login
    ), "redirect back to the jobs page"

@pytest.mark.test_logout_redirect_to_jobs
def test_login_redirect_to_jobs():
    assert "logout" in dir(app), "Create the `logout` function"
    assert "redirect" in dir(app), "`redirect` has not been imported from flask."
    assert "url_for" in dir(app), "`url_for` has not been imported from flask."
    assert "redirect:jobs:url_for" in get_functions(
        app.logout
    ), "redirect back to the jobs page"

