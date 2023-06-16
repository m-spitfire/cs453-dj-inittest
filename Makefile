generate:
	python3 autotest/runner.py -m many_models/manage.py -t many_models/test_app.py -c MyTestCase

test:
	python3 many_models/manage.py test test_app.MyTestCase

shell:
	python3 manage.py shell -i ipython

run:
	python3 manage.py runserver

evaluate:
	python3 evaluate.py
