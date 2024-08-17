My 23rd assignment! This is a flask application that uses SQLalchemy to streamline and simplify interaction with a fitness database which it creates. This is the same database I used in earlier projects, just refined. It has endpoints that allow for full CRUD and automatically creates the tables it needs provided the database exists. As a note for it's functionality, it will create the tables using ondelete='Cascade' on the foreign key "member_id" on workout_sessions, so that when a member is deleted the database itself will delete any would-be lingering entries.

Dependencies:  
1. Flask  
2. Flask-Marshmallow  
3. Flask-SQLalchemy  
4. MySQL-connector-python
5. SQLalchemy  

The project will also need both a database named 'fitness_database' (unless you change it in the program) with no tables, and a password.py with the database password in the root directory.

Endpoints for members:  
1. GET: localhost:5000/members  
2. GET: localhost:5000/members/id  
3. POST: localhost:5000/members  
4. PUT: localhost:5000/members/id  
5. DELETE: localhost:5000/members/id  

JSON structure:  
{
    "name": "John",
    "age": 29,
    "email": "john.doe@gmail.com",
    "phone": "1234567890"
}

---------------------------------------------------------

Endpoints for members:  
1. GET: localhost:5000/sessions  
2. GET: localhost:5000/sessions/id 
3. GET: localhost:5000/sessions_by_member/id 
4. POST: localhost:5000/sessions  
5. PUT: localhost:5000/sessions/id  
6. DELETE: localhost:5000/sessions/id  

JSON structure:  
{
    "activity": "Cardio",
    "member_id": "1",
    "session_date": "2024-07-23",
    "session_time": 830
}