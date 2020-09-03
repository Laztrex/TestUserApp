# User API 
(as a test task app)

## Description
Capability:  
- **Add User** 
~~~
POST:: http://localhost:5000/users
{'id': 42, 'name': 'Douglas Adams'}
~~~ 
- **Get list User**
~~~
GET:: http://localhost:5000/users
~~~ 
- **Get User by Id** 
~~~
GET:: http://localhost:5000/users/1
~~~ 
- **Edit User by Id**
 ~~~
PUT:: http://localhost:5000/users/1
{'name': Alexey}
~~~ 
- **Delete User by Id** 
~~~
DELETE:: http://localhost:5000/users/1
~~~ 
Run **option 1** (JSON format):
~~~
python main_json.py
~~~

**Run *expanded* option 2** (with Pony ORM and HTML-structure)
~~~
python __main__.py
~~~


Functionality and tests will be refined and expanded.