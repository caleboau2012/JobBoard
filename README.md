# Job Board with Python & Flask

## Requirements

- venv
- pip
- python

## Verify Local Environment

### Create Virtual Environment

In a terminal run the following commands from the root folder of the forked project.

Windows

```
python -m venv .\venv
```

macOS & Linux

```
python -m venv ./venv
```

OR

```
python3 -m venv ./venv
```

Once that completes, also run this command from the same folder.

Windows

```
venv\Scripts\activate.bat
```

macOS & Linux

```
source venv/bin/activate
```

Now that you are working in the virtualenv, install the project dependencies with the following command.

```
pip install -r requirements.txt
```

If you want to be able to add, delete and edit jobs, you should copy/rename the content of `.env.example` file to a file named `.env` and change the credentials as you deem fit. There are also other config variables you can change in the file.

### Verify Setup

In order to verify that everything is setup correctly, run the tests using the following command.

```
pytest
```

### Previewing Your Work

You can preview your work by running `flask run` in the root of your fork and then visit`http://localhost:5000` in your browser.

Alternatively, you can view this app live on http://job-board-flask.herokuapp.com/

To login to the admin, use
USERNAME=admin@jobboard.com
PASSWORD=ommletteDuFromage
