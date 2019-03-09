![Quikruit](Branding/logo.png?raw=true)

Developed for The University of Warwick Group Software Project, in association with Deutsche Bank. Won first prize upon presentation to the judges.

### Developed By:
* Jordan Field
* Alisha Patel
* Gowri Satish
* Tom Allton
* Cristian Virga
* Daniel Belo Goncalves 

This version of Quikruit contains some sample data, in order for you to see how the system can function later on in the life-cycle. All existing accounts have the password 'cs261group25'. You may log in to the recruiter site using these details:
* Email: admin@example.com
* Password: cs261group25

## Installation Instructions (Linux/Mac)
* Ensure Python 3 is installed on your computer.
    - e.g. on macOS type `brew install python3`.
* Open a terminal and navigate to the `quikruit` folder.
    - Note: _Not_ the `quikruit/quikruit` folder.
* Type `pip3 install -r requirements.txt` and press enter.
* Type `python3 manage.py runserver` and press enter. The server should start running.
* Access the applicant site at `localhost:8000/applicants` and the recruiter site at `localhost:8000/recruiters`.

## Installation Instructions (Windows)
* Ensure Python 3 is installed on your computer.
    - Python 3 for Windows can be installed from the Python website.
* Open a command propmt and navigate to the `quikruit` folder.
    - Note: _Not_ the `quikruit/quikruit` folder.
* Type `py -m pip install -r requirements.txt` and press enter.
* Type `py manage.py runserver` and press enter. The server should start running.
* Access the applicant site at `localhost:8000/applicants` and the recruiter site at `localhost:8000/recruiters`.

## Training shortcut
If you wish to train the ML model quickly. You can run the parser file to classify applicants from the sample dataset.

### Instructions
* Open the Django shell.
    - Linux/Mac: `python3 manage.py shell`
    - Windows: `py manage.py shell`
* Type `from dataset.parser import load; load()` and press enter.
* Press enter again when prompted to start the script.

## Questions shortcut
To automatically populate the TestQuestion table with placeholder questions. You may run the question generator function.

### Instructions:
* Open the Django shell.
    - Linux/Mac: `python3 manage.py shell`
    - Windows: `py manage.py shell`
* Type `from online_tests.generator import generate_questions; generate_questions()` and press enter.
* Press CTRL-C when You feel that sufficient questions have been generated.
