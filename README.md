
# MailMyTask >> Task Planner App

This is a web project in *Django Rest Framework* with name **MailMyTask**. it is a ***Task-Planner-App*** where user can register themselves, login, create project, cerate sub-section in a project and add task in sub section.

## Required files
 - .env
 - dbconfig.cnf

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`

`DEBUG`

`EMAIL`

`EMAIL_HOST`

`EMAIL_PORT`

`EMAIL_PASSWORD`
> Note: 
> If you want to use mysql as database then, to run this this project, you also need *dbconfig.cnf* file with database credentials. for more detail about *dbconfig.cnf* file ,please use [this documentation](https://docs.djangoproject.com/en/5.0/ref/databases/#mysql-notes). if you want you also can use sqlite as a database locally. to use sqlite please use this [django documentation](https://docs.djangoproject.com/en/5.0/ref/databases/#sqlite-notes)

## Setup Project Locally

Clone the project

```bash
  git clone https://github.com/Arunendrasingh/MailMyTask.git
```

Go to the project directory

```bash
  cd MailMyTask
```

Install dependencies

View [requirement.txt](./requirements.txt)

```bash
  pip install -r [requirement.txt]
```

Start the redis server
 > to install and use redis as broker please use [redis](https://redis.io/docs/) documentation.

Start the celery
 - on windows
```bash
  celery -A MailMyTask.celery worker -l DEBUG -E --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo
```
- on linux
```bash
  celery -A proj.celery worker -l INFO
```

Start flower to monitor celery task
```bash
 celery -A project --broker=redis://localhost:6379/0 flower
  
```
Start the Django server

```bash
  python manage.py runserver
```
 > use python3 in linux/macos

Now open url [http://127.0.0.1:8000](http://127.0.0.1:8000) to see project documentation.
Happy Coding


## Authors

- [@Arunendra Singh](https://www.github.com/arunendrasingh)

