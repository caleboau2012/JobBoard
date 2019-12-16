import pytest
import sys

from jobs import app
from .utils import (
    template_exists,
    template_data,
    template_extends,
    template_variables,
    template_functions,
    employer_for,
    get_functions,
    get_functions_returns,
    inspect,
)


@pytest.mark.test_employer_template
def test_employer_template():
    assert template_exists(
        "employer"
    ), "The `employer.html` template does not exist in the `templates` folder."
    el = template_data("employer").select(".box .media .media-content .content")
    assert len(el) == 1
    assert "layout.html" in template_extends(
        "employer"
    ), "The `employer.html` template does not extend `layout.html`."


@pytest.mark.test_employer_template_details
def test_employer_template_details():
    assert template_exists(
        "employer"
    ), "The `employer.html` template does not exist in the `templates` folder."
    assert "employer:name" in template_variables(
        "employer"
    ), "The `employer['name']` is not present in the template."
    assert "employer:description" in template_variables(
        "employer"
    ), "The `employer['description']` is not present in the template."


@pytest.mark.test_employer_template_all_jobs
def test_employer_template_all_jobs():
    assert template_exists(
        "employer"
    ), "The `employer.html` template does not exist in the `templates` folder."
    assert "show_jobs:jobs" in template_functions(
        "employer", "show_jobs"
    ), "Call the `show_jobs` macro in the `employer.html` file"


@pytest.mark.test_employer_template_reviews
def test_employer_template_reviews():
    assert template_exists(
        "employer"
    ), "The `employer.html` template does not exist in the `templates` folder."
    assert (
        "review:reviews" in employer_for()
    ), "Create a `for` loop that cycles through `reviews`"


@pytest.mark.test_employer_template_review_stars
def test_employer_template_review_stars():
    assert template_exists(
        "employer"
    ), "The `employer.html` template does not exist in the `templates` folder."
    assert (
        "_:range:0:review:rating" in employer_for()
    ), "Created a `for` loop that cycles through `reviews`"
    el = template_data("employer").select(".fa.fa-star.checked")
    assert len(el) == 1, "Add star `<span>` to the `employer.html` template"


@pytest.mark.test_employer_template_review_details
def test_employer_template_review_details():
    assert template_exists(
        "employer"
    ), "The `employer.html` template does not exist in the `templates` folder."
    assert "review:title" in template_variables(
        "employer"
    ), "The `review['title']` is not present in the template."
    assert "review:status" in template_variables(
        "employer"
    ), "The `review['status']` is not present in the template."
    assert "review:date" in template_variables(
        "employer"
    ), "The `review['date']` is not present in the template."
    assert "review:review" in template_variables(
        "employer"
    ), "The `review['review']` is not present in the template."


@pytest.mark.test_app_employer_route
def test_app_employer_route():
    assert "employer" in dir(app), "Create the `employer` function"
    assert "route:/employer/<employer_id>" in get_functions(app.employer)
    result = [
        item
        for item in get_functions(app.employer)
        if item.startswith("render_template:employer.html")
    ]
    assert len(result) == 1, "Call the `render_template` function."
    return_values = get_functions_returns(app.employer)[0]
    assert (
        return_values["value/args/s"] == "employer.html"
        and return_values["value/func/id"] == "render_template"
    ), "Return the `render_template` call"
    assert "employer:employer_id:job:employer_id" in template_functions(
        "_macros", "url_for"
    ), "The job title link `href` is incorrect in `_macros.html."


@pytest.mark.test_app_employer_route_employers
def test_app_employer_route_employers():
    assert "employer" in dir(app), "Create the `employer` function"
    assert (
        "employer_id" in inspect.getfullargspec(app.employer).args
    ), "Add the correct parameters to the `employer` function parameter list"
    execute_sql = (
        "execute_sql:SELECT * FROM employer WHERE id=?:employer_id:single:True"
    )
    execute_sql_alternate = (
        "execute_sql:SELECT * FROM employer WHERE id = ?:employer_id:single:True"
    )
    assert execute_sql in get_functions(
        app.employer
    ) or execute_sql_alternate in get_functions(
        app.employer
    ), "`execute_sql` has not been called or has the wrong parameters."
    result = [
        item
        for item in get_functions(app.employer)
        if item.startswith("render_template:employer.html:employer:employer")
    ]
    assert len(result) == 1, "Add `employer` to the `render_template` call."


@pytest.mark.test_app_employer_route_jobs
def test_app_employer_route_jobs():
    assert "employer" in dir(app), "Create the `employer` function"
    execute_sql = "execute_sql:SELECT job.id, job.title, job.description, job.salary FROM job JOIN employer ON employer.id = job.employer_id WHERE employer.id = ?:employer_id"
    assert execute_sql in get_functions(
        app.employer
    ), "`execute_sql` has not been called or has the wrong parameters."
    result = [
        item
        for item in get_functions(app.employer)
        if item.startswith("render_template:employer.html:employer:employer:jobs:jobs")
    ]
    assert len(result) == 1, "Add `jobs` to the `render_template` call."


@pytest.mark.test_app_employer_route_reviews
def test_app_employer_route_reviews():
    assert "employer" in dir(app), "Create the `employer` function"
    execute_sql = "execute_sql:SELECT review, rating, title, date, status FROM review JOIN employer ON employer.id = review.employer_id WHERE employer.id = ?:employer_id"
    assert execute_sql in get_functions(
        app.employer
    ), "`execute_sql` has not been called or has the wrong parameters."
    result = [
        item
        for item in get_functions(app.employer)
        if item.startswith(
            "render_template:employer.html:employer:employer:jobs:jobs:reviews:reviews"
        )
    ]
    assert len(result) == 1, "Add `reviews` to the `render_template` call."
