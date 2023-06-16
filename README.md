# Django Automated Testing Setup

![python version 3.10][badge/python]
[![black][badge/black]][repo/black]
[![isort][badge/isort]][isort]

## Submissions

- Presentation slides: [slides.pdf](docs/slides.pdf)
- Report: [report.pdf](docs/report.pdf)

## How to Run

```bash
$ python3 --version
Python 3.10.9

$ python3 -m venv .venv
$ source .venv/bin/activate
$ python3 -m pip install -r requirements.txt

$ python3 manage.py migrate

$ make generate
$ make evaluate
```

## Example Output

```bash
Ran 93 tests in 0.612s

OK
Name            Valid   Failed  Percentage
------------------------------------------
test_app        93      0       100.00%
------------------------------------------

Name                                     Stmts   Miss  Cover
------------------------------------------------------------
many_models/config/urls.py                   4      0   100%
many_models/employees/serializers.py        18      0   100%
many_models/employees/views.py             134     16    88%
many_models/manufacture/serializers.py      26      0   100%
many_models/manufacture/views.py           198     24    88%
------------------------------------------------------------
TOTAL                                      380     40    89%
```

[badge/black]: https://img.shields.io/badge/code%20style-black-000000
[badge/isort]: https://img.shields.io/badge/%20imports-isort-%231674b1?labelColor=ef8336
[badge/python]: https://img.shields.io/badge/python-3.10-blue
[isort]: https://pycqa.github.io/isort
[repo/black]: https://github.com/psf/black
