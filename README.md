## fva [![Build Status](https://travis-ci.org/uncleabbey/fva.svg?branch=master)](https://travis-ci.org/uncleabbey/fva) [![Coverage Status](https://coveralls.io/repos/github/uncleabbey/fva/badge.svg)](https://coveralls.io/github/uncleabbey/fva)


## Food Vendor Backend App

This is Venture Gardens Group(VGC) Internship capstone project for backend interns (Python/Django Stack)

## (Documentation)[https://kayode-foodvendor.herokuapp.com/]

Swagger Documentation for the project can be found (Here....)[https://kayode-foodvendor.herokuapp.com/]


#### APP URL: https://kayode-foodvendor.herokuapp.com/docs


## How to run locally
* clone the repo using `git clone https://github.com/uncleabbey/fva`
* Set a virtual environment using virtualenv or venv or pipenv
* run `pip install -r requirements.txt` to install needed dependency
* create a .env file  and create env variables like 

```
DEBUG=True
DATABASE_URL=_postgress_database_url
SECRET_KEY=your_secret_key
```
* run `python manage.py migrate` to migrate the tables
* run server using `python manage.py runserver`
 


## How it Works
Register a new user using (Customer Registeration)[https://kayode-foodvendor.herokuapp.com/api/auth/signup/customer] or (Vendor Registration)
[https://kayode-foodvendor.herokuapp.com/api/auth/signup/vendor]

or quickly use the following test users for quick (Login)[https://kayode-foodvendor.herokuapp.com/api/auth/login] if you don't want to gpo through registration stress
Vendor email: johndoe@gmail.com
password: some_strong_password


Customer email: janedoe@gmail.com
password: some_strong_password

If you have any question using this app, contact Phone Number: 07069388069 or Email: kayodegabriela@gmail.com