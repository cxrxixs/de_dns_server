### Setup

0. (Optional) Install virtual env and activate it.
  ```
  pip3 install virtualenv
  virtualenv venv
  source venv/bin/activate
```

1. Install the requirements for the project.

```
pip install -r requirements.txt
pip install psycopg2-binary
pip install psycopg2
```

2. In the provided database host from the test file, create a database with name of the following format `<your surname>_<your birthdate in MMDD>`. You will use this database in the next step.

3. In `jpd_test` folder, copy `.env-dist` file to a file on the same folder with name `.env`. Fill up each environment variable with values. These will be used to determine the database your Django project will connect to.

4. Run django migrations to prepare your database.
```
python manage.py migrate
```

    - Confirm that this worked by checking that `de_dns_servers` table have been created in your database.

5. Run the server
```
python manage.py runserver
```

6. Go to your browser and access ```localhost:8000/de-dns-servers```. You should see a page that says 'No dns servers are available.'
