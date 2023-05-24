generate:
	python autotest/runner.py -m manage.py -t test_app.py -c MyTestCase

test:
	python manage.py test test_app.MyTestCase