generate:
	python autotest/runner.py -m simple_app/manage.py -t simple_app/test_app.py -c MyTestCase

test:
	python manage.py test test_app.MyTestCase
