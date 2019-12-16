import pytest
import sys

from jobs import app
from .utils import (
    template_exists,
    template_macros,
    template_macro_soup,
    template_variables,
    show_jobs_for,
    template_import,
    template_data,
    template_functions,
    get_functions,
)


@pytest.mark.test_template_macros
def test_template_macros():
    assert template_exists(
        "_macros"
    ), "The `_macros.html` template does not exist in the `templates` folder."


@pytest.mark.test_show_job_macro_definition
def test_show_job_macro_definition():
    assert template_exists(
        "_macros"
    ), "The `_macros.html` template does not exist in the `templates` folder."
    assert "show_job:job" in template_macros(
        "_macros"
    ), "Create the `show_job` macro and add the correct parameter"


@pytest.mark.test_show_job_macro_html
def test_show_job_macro_html():
    assert template_exists(
        "_macros"
    ), "The `_macros.html` template does not exist in the `templates` folder."
    html = template_macro_soup("_macros", "show_job")
    p = html.select(".card .card-header .card-header-title")
    div = html.select(".card-content .content")
    assert len(p) == 1 and len(div) == 1


@pytest.mark.test_show_job_macro_header
def test_show_job_macro_header():
    assert template_exists(
        "_macros"
    ), "The `_macros.html` template does not exist in the `templates` folder."
    assert "job:title" in template_variables(
        "_macros"
    ), "The job title link does not have content."


@pytest.mark.test_show_job_macro_body
def test_show_job_macro_body():
    assert template_exists(
        "_macros"
    ), "The `_macros.html` template does not exist in the `templates` folder."
    assert "job:employer_name" in template_variables(
        "_macros"
    ), "Not showing the employer name"
    assert "job:salary" in template_variables("_macros"), "Not showing the job salary"
    assert "job:description" in template_variables(
        "_macros"
    ), "Not showing the job description"


@pytest.mark.test_show_jobs_macro_definition
def test_show_jobs_macro_definition():
    assert template_exists(
        "_macros"
    ), "The `_macros.html` template does not exist in the `templates` folder."
    assert "show_jobs:jobs" in template_macros(
        "_macros"
    ), "Create the `show_jobs` macro and added the correct parameter"


@pytest.mark.test_show_jobs_macro_for_loop
def test_show_jobs_macro_for_loop():
    assert template_exists(
        "_macros"
    ), "The `_macros.html` template does not exist in the `templates` folder."
    assert "show_jobs:jobs" in template_macros(
        "_macros"
    ), "Create the `show_jobs` macro and added the correct parameter"
    html = template_macro_soup("_macros", "show_jobs")
    div = html.select("div.columns.is-multiline")
    assert len(div) == 1
    assert "job:jobs" in show_jobs_for()


@pytest.mark.test_show_jobs_macro_for_loop_body
def test_show_jobs_macro_for_loop_body():
    assert template_exists(
        "_macros"
    ), "The `_macros.html` template does not exist in the `templates` folder."
    assert "show_jobs:jobs" in template_macros(
        "_macros"
    ), "Create the `show_jobs` macro and added the correct parameter"
    html = template_macro_soup("_macros", "show_jobs")
    div = html.select("div.column.is-half")
    assert len(div) == 1
    assert "show_job:job" in show_jobs_for()


@pytest.mark.test_import_macros
def test_import_macros():
    assert template_exists(
        "_macros"
    ), "The `_macros.html` template does not exist in the `templates` folder."
    assert "_macros.html:show_job:show_jobs:True" == template_import(
        "layout"
    ), "Import `_macros.html` in `layout.html`"


@pytest.mark.test_index_template
def test_index_template():
    assert template_exists(
        "index"
    ), "The `index.html` template does not exist in the `templates` folder."
    el = template_data("index").select(".columns .column.is-one-fifth")
    assert len(el) == 1


@pytest.mark.test_display_all_jobs
def test_display_all_jobs():
    assert template_exists(
        "index"
    ), "The `index.html` template does not exist in the `templates` folder."
    assert "show_jobs:jobs" in template_functions(
        "index", "show_jobs"
    ), "Call the `show_jobs` macro in the `index.html` file"
