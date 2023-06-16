# PROJECT = cycle_simple
# PROJECT = simple_app
PROJECT = many_models
# PROJECT = reddit

generate:
	python3 autotest/runner.py -m $(PROJECT)/manage.py -t $(PROJECT)/test_app.py -c MyTestCase

test:
	python3 $(PROJECT)/manage.py test test_app.MyTestCase

shell:
	python3 manage.py shell -i ipython

run:
	python3 manage.py runserver

evaluate:
	python3 $(PROJECT)/evaluate.py

coverage:
	coverage html

migrate:
	python3 $(PROJECT)/manage.py makemigrations
	python3 $(PROJECT)/manage.py migrate
