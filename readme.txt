TODDLE TASK SUBMISSION

Name: Utkarsh Aditya        
Task: Backend
-------------------------------------------------------------------------------------------------
INSTRUCTIONS TO RUN

1. Create a virtual environment and run it.
2. Run following command -> pip install requirements.txt
3. Run following command -> python manage.py runserver
4. In browser, go to URL -> http://127.0.0.1:8000/docs/
5. To get JWT, use "/api/token/" and click on "Try it out"
   For username and password use one of the following credentials. NOTE : If you put incorrect credentials you won't get authorized for further requests.
    
    USERNAME                PASSWORD                ROLE   
A.  utkarshaditya01         admin                   student
B.  tutor01                 admin                   tutor
C.  admin                   admin                   superuser       (use this account to create new students or tutors from django admin page)
D.  ashu01                  admin                   student
E.  tutor02                 admin                   tutor

6. After entering credentials, click on execute, copy the "access" token from "response body". This will be used for authorizing further requests.
7. Click on "authorize" on top right side of the docs page. Type the token in the format -> "Bearer TOKEN" where TOKEN is from step 6.
8. Now according to the role you will be able to try out rest of the APIs on the docs page. 

Note: I have set the token lifetime as 500 mins, it can be changed from settings.py
------------------------------------------------------------------------------------------------------------
IMPORTANT

All required SQL files are in the folder.
ER Diagram of RDBMS is there in the folder.
Swagger YAML file is there in the folder, you can just run the docs page since all the APIs could be tried there easily.
------------------------------------------------------------------------------------------------------------
BONUS

Deployed - https://virtualclassroomutkarsh.herokuapp.com/docs/

Attempted Notification System

NOTE : While creating student or tutor use the following password -> "pbkdf2_sha256$260000$9i1UafjXzqDhLdEW3Wg5CW$w3Vu5mlX2NAV3d6KF4DO/s9Z8ae+s2Dyue29YLmdJDg="
since its salted hash of "admin"
