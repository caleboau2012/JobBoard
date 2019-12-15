import datetime, os
from flask import Flask, render_template, g, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from .util import execute_sql, allowed_file

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "resumes")
ADMIN = (os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD"))

app = Flask(__name__)
app.secret_key = "1234567890"

# create the folders when setting up your app
os.makedirs(os.path.join(app.instance_path, UPLOAD_FOLDER), exist_ok=True)


@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, "_connection", None)
    if connection != None:
        connection.close()


@app.route("/")
@app.route("/jobs")
def jobs():
    jobs = execute_sql(
        "SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id ORDER BY job.id DESC"
    )
    return render_template("index.html", jobs=jobs)


@app.route("/job/<job_id>")
def job(job_id):
    job = execute_sql(
        "SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?",
        [job_id],
        single=True,
    )
    return render_template("job.html", job=job)


@app.route("/employer/<employer_id>")
def employer(employer_id):
    employer = execute_sql(
        "SELECT * FROM employer WHERE id=?", [employer_id], single=True
    )
    jobs = execute_sql(
        "SELECT job.id, job.title, job.description, job.salary FROM job JOIN employer ON employer.id = job.employer_id WHERE employer.id = ?",
        [employer_id],
    )
    reviews = execute_sql(
        "SELECT review, rating, title, date, status FROM review JOIN employer ON employer.id = review.employer_id WHERE employer.id = ?",
        [employer_id],
    )
    return render_template(
        "employer.html", employer=employer, jobs=jobs, reviews=reviews
    )


@app.route("/employer/<employer_id>/review", methods=("GET", "POST"))
def review(employer_id):
    if request.method == "POST":
        review = request.form["review"]
        rating = request.form["rating"]
        title = request.form["title"]
        status = request.form["status"]
        date = datetime.datetime.now().strftime("%m/%d/%Y")

        execute_sql(
            "INSERT INTO review (review, rating, title, date, status, employer_id) VALUES (?, ?, ?, ?, ?, ?)",
            (review, rating, title, date, status, employer_id),
            commit=True,
        )

        return redirect(url_for("employer", employer_id=employer_id))

    jobs = execute_sql(
        "SELECT job.id, job.title, job.description, job.salary FROM job JOIN employer ON employer.id = job.employer_id WHERE employer.id = ?",
        [employer_id],
    )
    employer = execute_sql(
        "SELECT * FROM employer WHERE id=?", [employer_id], single=True
    )
    return render_template("review.html", employer=employer, jobs=jobs)


@app.route("/jobs/<job_id>/apply/", methods=("GET", "POST"))
@app.route("/jobs/<job_id>/apply/<complete>", methods=("GET", "POST"))
def apply(job_id, complete=False):
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file uploaded")
            return redirect(request.url)

        file = request.files["file"]
        # if user does not select file, the browser would also
        # submit an empty part without filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.instance_path, UPLOAD_FOLDER, filename))

        name = request.form["name"]
        cover_letter = request.form["cover_letter"]
        date = datetime.datetime.now().strftime("%m/%d/%Y")

        execute_sql(
            "INSERT INTO application (name, cover_letter, date, file_name, job_id) VALUES (?, ?, ?, ?, ?)",
            (name, cover_letter, date, file.filename, job_id),
            commit=True,
        )

        return redirect(url_for("apply", job_id=job_id, complete="done"))

    job = execute_sql(
        "SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?",
        [job_id],
        single=True,
    )
    return render_template("apply.html", job=job, complete=complete)


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email == ADMIN[0] and password == ADMIN[1]:
            session["logged_in"] = True
            return redirect(url_for("jobs"))

        flash("Incorrect login credentials")
        return redirect(request.url)

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("logged_in")
    return redirect(url_for("jobs"))


@app.route("/jobs/edit/<job_id>", methods=("GET", "POST"))
@app.route("/jobs/add", methods=("GET", "POST"))
def add(job_id=None):
    if "logged_in" not in session:
        return redirect(url_for("jobs"))

    if request.method == "POST":
        title = request.form["title"]
        employer_id = request.form["employer"]
        salary = request.form["salary"]
        description = request.form["description"]

        if job_id:
            execute_sql(
                "UPDATE job SET title=?, description=?, salary=?, employer_id=? WHERE id = ?",
                (title, description, salary, employer_id, job_id),
                commit=True,
            )
        else:
            execute_sql(
                "INSERT INTO job (title, description, salary, employer_id) VALUES (?, ?, ?, ?)",
                (title, description, salary, employer_id),
                commit=True,
            )

        return redirect(url_for("jobs"))
    job = execute_sql(
        "SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?",
        [job_id],
        single=True,
    )
    employers = execute_sql("SELECT * FROM employer")
    return render_template("add.html", job=job, employers=employers)


@app.route("/jobs/delete/<job_id>")
def delete(job_id):
    execute_sql(
        "DELETE FROM job WHERE id = ?", [job_id], commit=True,
    )
    return redirect(url_for("jobs"))
