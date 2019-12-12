import pytest
import sys

from jobs import app
from .utils import (
    template_exists,
    template_extends,
    template_block,
    template_functions,
    get_functions,
    get_functions_returns,
    inspect,
)


@pytest.mark.test_app_job_template
def test_app_job_template():
    assert template_exists(
        "job"
    ), "The `job.html` template does not exist in the `templates` folder."
    assert "layout.html" in template_extends(
        "job"
    ), "The `job.html` template does not extend `layout.html`."
    assert "content" in template_block(
        "job"
    ), "Have you added a template `block` called `content`?"
    assert "show_job:job" in template_functions(
        "job", "show_job"
    ), "Call the `show_job` macro in the `job.html` file"


@pytest.mark.test_app_job_route
def test_app_job_route():
    assert "job" in dir(app), "Create the `job` function"
    result = [
        item
        for item in get_functions(app.job)
        if item.startswith("render_template:job.html")
    ]
    assert len(result) == 1, "Call the `render_template` function."
    return_values = get_functions_returns(app.job)[0]
    assert (
        return_values["value/args/s"] == "job.html"
        and return_values["value/func/id"] == "render_template"
    ), "Return the `render_template` call"


@pytest.mark.test_app_job_route_decorator
def test_app_job_route_decorator():
    assert "job" in dir(app), "Create the `job` function?"
    assert "route:/job/<job_id>" in get_functions(
        app.job
    ), "Add a `job_id` parameter to the job function"


@pytest.mark.test_app_job_route_parameter
def test_app_job_route_parameter():
    assert "job" in dir(app), "Create the `job` function"
    assert "job:job_id:job:id" in template_functions(
        "_macros", "url_for"
    ), "The job title link `href` is incorrect."
    assert (
        "job_id" in inspect.getfullargspec(app.job).args
    ), "Add the correct parameters to the `job` function parameters list"


@pytest.mark.test_app_job_route_data
def test_app_job_route_data():
    assert "job" in dir(app), "Create the `job` function"
    execute_sql = "execute_sql:SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?:job_id:single:True"
    assert execute_sql in get_functions(
        app.job
    ), "`execute_sql` has not been called or has the wrong parameters."


@pytest.mark.test_app_job_route_pass_data
def test_app_job_route_pass_data():
    assert "job" in dir(app), "Create the `job` function"
    assert "render_template:job.html:job:job" in get_functions(
        app.job
    ), "Add `job` to the `render_template` call."


@pytest.mark.test_app_jobs_route_jobs
def test_app_jobs_route_jobs():
    assert "jobs" in dir(app), "Create the `jobs` function"
    assert "render_template:index.html:jobs:jobs" in get_functions(
        app.jobs
    ), "Add `jobs` to the `render_template` call."
