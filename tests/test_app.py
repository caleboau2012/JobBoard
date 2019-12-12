import pytest
import inspect

from jobs import app
from .utils import get_decorators, get_functions


@pytest.mark.test_app_import_g
def test_app_import_g():
    assert "g" in dir(app), "Import the `g` class from `flask`?"


@pytest.mark.test_app_close_connection
def test_app_close_connection():
    assert "close_connection" in dir(app), "Define a function named `close_connection`."
    assert "close" in get_functions(
        app.execute_sql
    ), "Call the `close` function in `execute_sql`?"


@pytest.mark.test_app_close_connection_decorator
def test_app_close_connection_decorator():
    assert "close_connection" in dir(app), "Define a function named `close_connection`."
    decorators = get_decorators(app.close_connection)["close_connection"]
    assert len(decorators) == 1, "Add the correct decorator to `close_connection`."
    decorator = decorators[0][0]
    assert (
        decorator == "teardown_appcontext"
    ), "`close_connection` doesn't have a `teardown_appcontext` decorator?"
