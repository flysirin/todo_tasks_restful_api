# Todo tasks RESTful API  
This is an example of how to build a RESTful API that performs CRUD operations on a MySQL database using Flask and the extension, Flask-RESTful.
The particular application is creating a to-do list. Flexible settings for database configurations with Application Factories.


# Link to my GitHub
https://github.com/flysirin/todo_tasks_restful_api

## Contents:
**app.py** - Defines the flask app, and the Flask RESTful api endpoints defined on top of it     
**models.py** - Defines the data model, implemented with the Flask SQLAlchemy ORM
**error_handlers.py** - error handlers when working with the database
**config.py** - Configuration file with parameters loaded from **.env**   
**configmodule.py** - configuration classes for accessing the database and for flexible changes to server settings
**create_db.py** - Create database  
**tests.py** - Testing of API endpoints using Python unittest module   


## How to use:

Set up your database and launch it, more details here:  
https://dev.mysql.com/doc/mysql-getting-started/en/

Make sure, that you are using the correct credentials to access the database

Change login, password, host, port and database credential, if you need in   **.env**

**_Attention! Using configurations to set up a database like DevelopmentConfig, ProductionConfig in tests.py
may lead to data deletion. Use TestingConfig or create your own setup classes for tests_**  

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

GET all tasks:  
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

##Flask-RESTful:

Simplicity and Structure: Flask-RESTful provides a straightforward way to structure RESTful APIs in Flask. It encourages a clear and consistent organization of resources using classes as resources.
Request Parsing: The library comes with a built-in request parsing mechanism (reqparse), making it easier to handle and validate incoming JSON data or form data.
Marshaling: Flask-RESTful includes support for object serialization, helping in transforming complex data types into JSON responses.
Justification:

Chose Flask-RESTful for its simplicity in structuring RESTful APIs and built-in tools like reqparse and marshaling, making it easier to handle and validate incoming requests and format responses consistently.

##Flask-HTTPAuth:  

Authentication Support: Flask-HTTPAuth simplifies the implementation of authentication mechanisms in Flask applications. It provides decorators for protecting specific routes or resources.
Basic HTTP Authentication: If your project requires basic HTTP authentication, Flask-HTTPAuth seamlessly integrates with Flask applications.
Customizable: It allows for customization, allowing you to implement authentication strategies that suit your project requirements.
Justification:  
Integrated Flask-HTTPAuth to easily implement authentication in our Flask project. It's support for various authentication mechanisms and customization options made it the right choice for securing our API endpoints.  


**Flask-RESTful documentation**      
Definitely read through the docs before building your own API. Start with the quickstart API
and then move on to using argument parsing and field marshaling. Be aware that the API reference page
is currently empty, and that there are other typos in the docs. Also, the `reqparse` functionality is being deprecated
in favor of the external `marshmallow` package. I found that there weren't enough examples in the docs to figure out how to fit all of the components together
in one app, but the docs were useful to refer to after looking at other examples. 
https://flask-restful.readthedocs.io/en/latest/


##Application Factories
1) Testing. You can have instances of the application with different settings to test every case.

2) Multiple instances. Imagine you want to run different versions of the same application. Of course you could have 
multiple instances with different configs set up in your webserver, but if you use factories, you can have multiple
instances of the same application running in the same application process which can be handy.
https://flask.palletsprojects.com/en/2.3.x/patterns/appfactories/
