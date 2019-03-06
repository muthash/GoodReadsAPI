## GoodReadsAPI

Goodreads API provides a platform for users to share the titles or genres they’ve enjoyed in the past or planning to read in the future. Specifically:
- Register for an account
- Login into registered account
- Create book entries 
- Update the status of a book
- View all Book entries
- View single Book entry

### Prerequisites

- Python 3.6 or a later version
- PostgreSQL

##E Installation

Clone the repo.
```
$ git clone https://github.com/muthash/GoodReadsAPI.git
```
and cd into the folder:
```
$ /GoodReadsAPI
```

### Virtual environment

Create a virtual environment:
```
python3 -m venv venv
```
Activate the environment
```
$ source venv/bin/activate
```

### Dependencies

Install package requirements to your environment.
```
pip install -r requirements.txt
```

### Env

Create a .env file in your Weconnect-api  root directory and add
```
source venv/bin/activate
export FLASK_APP="run.py"
export FLASK_ENV="development"
export SECRET="some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING"
export DATABASE_URL="postgresql://username:password@localhost/database_name"
export TEST_DATABASE_URL="postgresql://username:password@localhost/test_database_name"
```

activate the environment
```
source .env
```

### Database migration

Create two Databases in PostgreSQL:
- production database
- testing database

Run the following commands for each database:
```
python manager.py db init

python manager.py db migrate

python manager.py db upgrade

```

### Testing

To set up unit testing environment:
```
$ pip install nose
$ pip install coverage
```

To run tests perform the following:
```
$ nosetests --with-coverage
```

### Start The Server

To start the server run the following command
```
flask run
```
The server will run on http://127.0.0.1:5000/

### Testing API on Postman

*Note* Ensure that after you succesfully login a user, you use the generated token in the authorization header for the endpoints that require authentication. Remeber to add Bearer before the token as shown:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9eyJpYXQiO 
```

### API endpoints

| Endpoint | Method |  Functionality | Authentication |
| --- | --- | --- | --- |
| /auth/register | POST | Creates a user account | FALSE
| /auth/login | POST | Logs in a user | FALSE
| /books | POST | Create a book entry | TRUE
| /books | GET | Retrieves all book entries| OPTIONAL 
| /books/{shelfid} | GET | Retrieve a single book entry | OPTIONAL
| /books/{shelfid} | PATCH | Update a book status | TRUE
