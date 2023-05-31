generate:
	python3 autotest/runner.py -m manage.py -t test_app.py -c MyTestCase

test:
	python3 manage.py test test_app.MyTestCase

shell:
	python3 manage.py shell -i ipython

run:
	python3 manage.py runserver
