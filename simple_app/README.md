# Django Automated Testing Setup

![python version 3.10][badge/python]
[![black][badge/black]][repo/black]
[![isort][badge/isort]][isort]

## How to Run

```bash
$ python3 --version
Python 3.10.9

$ python3 -m venv .venv
$ source .venv/bin/activate
$ python3 -m pip install -r requirements.txt

$ python3 manage.py migrate

$ python3 manage.py createsuperuser
Username (leave blank to use 'root'): admin
Email address: admin@example.com
Password:
Password (again):
Superuser created successfully.

$ python3 manage.py runserver
```

It will start the webserver on port `8000`.

The API documentation can be accessed via `http://localhost:8000/api/schema/swagger-ui`

[badge/black]: https://img.shields.io/badge/code%20style-black-000000
[badge/isort]: https://img.shields.io/badge/%20imports-isort-%231674b1?labelColor=ef8336
[badge/python]: https://img.shields.io/badge/python-3.10-blue
[isort]: https://pycqa.github.io/isort
[repo/black]: https://github.com/psf/black
