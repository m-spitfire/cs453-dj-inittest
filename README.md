```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser email=admin@example.com username=admin
./manage.py runserver
```
It will start webserver at port `8000`.

The API documentation can be accessed via `http://localhost:8000/api/schema/swagger-ui`
