#CRUD Task 
This project is a CRUD (Create, Read, Update, Delete) 
users management application built using FastAPI and PostgreSQL. 
It provides a RESTful API to manage users, allowing users to create, retrieve, update, 
and delete user data.

Features
* Create users: Users can create new users by providing their username and email.
* Retrieve user data: Users can retrieve the details of existing users by their unique identifiers.   
* Update users: Users can update the details of users, including their username and email.    
* Delete users: Users can delete users by their unique identifiers.   

Installation Requirements
 - Docker      

Getting Started  
To build and run the project, follow these steps:   

- Build the project: make build   
- Start the project: make start   
- Stop the project: make stop 
- Remove database artifacts: make clean   
- Restart the project (build and start): make restart 
- Start tests (after project start): make test    

API request examples can be found in the "CRUD_task.postman_collection.json" in root folder.    
Swagger can be found in the "swagger.json" in root folder.

For more information about the API, run the app and open the following links:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc