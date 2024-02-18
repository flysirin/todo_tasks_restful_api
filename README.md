# todo-api
This is an example of how to build a RESTful API that performs CRUD operations on a Sqlite database using Flask and the extension, Flask-RESTful.
The particular application is creating a to-do list.

## Contents:
**app.py** - Defines the flask app, and the Flask RESTful api endpoints defined on top of it     
**models.py** - Defines the data model, implemented with the Flask SQLAlchemy ORM    
**config.py** - Testing of API endpoints using Python unittest module  
**tests.py** - Configuration file with parameters loaded from **.env**  
**create_db.py** - Create database  

## How to use:
Change login, password, host, port, database name, if you need in   **.env**

Install requirements
```
pip install -r requirements.txt
```

Create database
```
python3 create_db.py
```
Run server
```
python3 app.py
```

To access the api from the command line:

GET request (for task with id 1):
```
curl -u login:pass http://localhost:5000/todo/1

```

GET all requests:  
```
curl -u login:pass http://localhost:5000/todo

```
POST request:
```
curl -u login:pass http://localhost:5000/todo -X POST -H "Content-Type:application/json" -d '{"title":"New task","description":"ToDo something"}'
```

PUT request:
```
curl -X PUT -u login:pass -H "Content-Type: application/json" -d '{"title": "Updated Title", "description": "Updated Description"}' http://localhost:5000/todo/1
```

DELETE request:
```
curl -X DELETE -u login:pass http://localhost:5000/todo/1
```



**Flask-RESTful documentation**      
Definitely read through the docs before building your own API. Start with the quickstart API
and then move on to using argument parsing and field marshaling. Be aware that the API reference page
is currently empty, and that there are other typos in the docs. Also, the `reqparse` functionality is being deprecated
in favor of the external `marshmallow` package. I found that there weren't enough examples in the docs to figure out how to fit all of the components together
in one app, but the docs were useful to refer to after looking at other examples. 
https://flask-restful.readthedocs.io/en/latest/
