import pytest
import inspect

from jobs import util
from .utils import os, get_functions, get_statements


@pytest.mark.test_util_import_sqlite
def test_util_import_sqlite():
    assert "sqlite3" in dir(util), "Import `sqlite`"


@pytest.mark.test_util_import_g
def test_util_import_g():
    assert "g" in dir(util), "Import the `g` class from `flask`"


@pytest.mark.test_util_db_path
def test_util_db_path_module3():
    assert "PATH" in dir(util), "Create a constant called `PATH`."
    assert util.PATH == "db/jobs.sqlite", "Create a constant called `PATH`"


@pytest.mark.test_util_open_connection_get_attribute
def test_util_open_connection_get_attribute():
    assert "open_connection" in dir(util), "Define a function named `open_connection`."
    assert "getattr:g:_connection:None" in get_functions(
        util.open_connection
    ), "Use the `getattr` function to get the global `_connection`"


@pytest.mark.test_util_open_connection_connection
def test_util_open_connection_connection():
    assert "g" in dir(util), "Import the `g` class from `flask`"
    assert "open_connection" in dir(util), "Define a function named `open_connection`."


@pytest.mark.test_util_open_connection_row_factory
def test_util_open_connection_row_factory():
    assert "g" in dir(util), "Import the `g` class from `flask`"
    assert "open_connection" in dir(util), "Define a function named `open_connection`."


@pytest.mark.test_util_execute_sql
def test_util_execute_sql():
    assert "execute_sql" in dir(util), "Defined a function named `execute_sql`."
    assert "open_connection" in get_functions(
        util.execute_sql
    ), "Call the `open_connection` function in `execute_sql`"


@pytest.mark.test_util_execute_sql_parameters
def test_util_execute_sql_parameters():
    assert "execute_sql" in dir(util), "Define a function named `execute_sql`."
    parameters = inspect.getfullargspec(util.execute_sql)
    assert len(parameters.args) == 4, "Add parameters to the `execute_sql` function."
    assert (
        parameters.args[0] == "sql"
        and parameters.args[1] == "values"
        and parameters.args[2] == "commit"
        and parameters.args[3] == "single"
    ), "Add the correct parameters to the `execute_sql` function parameters list"
    assert (
        parameters.defaults[0] == ()
        and parameters.defaults[1] == False
        and parameters.defaults[2] == False
    ), "`args` and `one` parameters have the correct defaults in the `execute_sql` function parameters list"


@pytest.mark.test_util_execute_sql_execute
def test_util_execute_sql_execute():
    assert "execute_sql" in dir(util), "Define a function named `execute_sql`."
    assert "execute:sql:values" in get_functions(
        util.execute_sql
    ), "Call the `execute` function in `execute_sql`"


@pytest.mark.test_util_execute_sql_results
def test_util_execute_sql_results():
    assert "execute_sql" in dir(
        util
    ), "Have you defined a function named `execute_sql`."
    assert "fetchall" in get_functions(
        util.execute_sql
    ), "Have you called the `fetchall` function in `execute_sql`"
    assert "fetchone" in get_functions(
        util.execute_sql
    ), "Have you called the `fetchone` function in `execute_sql`"
    assert "commit" in get_functions(
        util.execute_sql
    ), "Have you called the `close` function in `execute_sql`"
    assert "close" in get_functions(
        util.execute_sql
    ), "Have you called the `close` function in `execute_sql`"
    assert (
        len(get_statements(util.execute_sql)) >= 0
    ), "Have created an if statement in the `execute_sql` function"
    assert (
        "results" == get_statements(util.execute_sql)[0]["body/targets/id"]
    ), "Have you assigned the `results` variable to `connection.commit()`"
