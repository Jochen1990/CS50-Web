# Final Project CS50 Web Capstone - Polly, a simple survey website

## General
In my final project for CS50 Web-Capstone, I created a web app called 'Polly - A simple survey website'.
The idea is, that a user can register for the website and is then able to create surveys, vote on surveys (on his or her own and surveys created by others) and close surveys to be able to see the results of the survey, once the author feels, that a sufficient quantity of votes are in.

The web app uses the django framework for web apps, as introduced in the CS50 Web course. The web app uses in total 3 SQL models: the user model, a 'survey' model and a 'vote' model.

In total, there are 8 templates (including the layout.html) which include an index page, a login page, a 'new survey' page, a 'profile' page, a 'register' page, a 'results' page and a 'surveys' page.

The views.py file includes 8 distinct functions (index, login, logout, register, new_survey, surveys, profile, results) that call and render the templates with the needed information to display the correct data.

## Distinctiveness and Complexity
The 'Polly - A simple survey website' is distinct from the other projects in this course, because it is neither a network nor a mail client, nor like any other project in the CS50 Web course. The survey website uses three models, of which only the User model is identical to the use rmodel used in other projects. The survey webapp uses two other models, that are significantly distinct from other models used in other projects in this course. The models used are explained in more detail below under the chapter 'Python files - models.py'.
Also the functions used in the webapp are different than in the other projects. Only the login and register function are the same as used in the other projects. All other functions are very distinct and unique in their way of interacting with the templates. The functions used are explained in more detail below in the chapter 'Python files - views.py'. The project also uses other bootstrap styling, its own javascript static file and a unique CSS class for the survey divs.
The webapp is more complex than other projects in the course, because the webapp is based on a model which ultimately needs to be used to do calculations on the votes. This has not been done in any other project of the course.
A more detailed view on the distinctiveness and complexity of the webapp is shown in the following chapters which explain the content of all used files, models, functions etc.

### Detailed View on the Files

#### Static
The static folder in this webapp contains two files. The index.js file and the styles.css file.

##### Index.js
The index.js file consists of a javascript function, which is used on the 'new survey' page (explained further down below). It makes sure, that the user inputs at least a question and two answers. Otherwise the user is prompted with an alert, that she or he must provide the necessary information to create the survey. This is achieved by accessing the values of the form inputs and checking if they are equal to 'null' or empty.

##### Styles.css
The styles.css consists of a class which defines the look of the surveys, that are displayed on the various templates, see below. It effectively designes a box for each survey, by defining a border, the display attribute, margin etc.


#### Templates
Below the templates used in the web app and their content are explained in detail.

##### Layout.html
The 'layout.html' file in the 'templates' folder defines the look of all of the pages of the webapp. It contains a head which includes link references and script references to the bootstrap framework. Bootstrap is used in the layout.html file to give all of the pages a unique look. Furthermore, in the body of layout.html, the coarse look of all of the pages is defined. There is a navbar at the top of the page which includes all of the routes' links. Additionally, several routes are only displayed, when the user is signed in.

##### Index.html
The 'index' template extendes the 'layout.html' file and loads the static files (index.js and styles.css). It consists of a block body which contains several paragraphs, that explain the webapp. The index page is built very simply, because it is only meant to be a landing page, that explains the webapp to the user.

##### Login.html
The 'login' template can only be reached if no user is logged in. This is achieved in the layout.html file by checking if the user is authenticated. If the user is not, the link to the login route is shown in the navbar at the top. The login template extends the 'layout.html' file to inherit the design. It has a block body, which includes a header, a form for the user to type in her or his credentials and a link to the register route, in case the user has not registered yet. In case of wrong or missing credentials, the user is shown an error message. The form on the site interacts with a dedicated function in the 'views.py' file.

##### Register.html
If the user does not have an account yet, she or he is able to create an account either by clicking on 'register' in the navbar or by clicking on 'register here' in the login route. The 'register' template hereby again extends the 'layout.html' template to inherit the design and the bootstrap funcionality. The form on the site interacts with a dedicated function in the 'views.py' file, which renders an error message if the username is already taken e.g. Also the function stores the information in a SQL file which is defined by the user model in models.py.

##### Profile.html
The profile.html template extends the layout.html file to inherit the design. It has a block body which displays (if there are any) all surveys, that the uiser has created. This is achieved by interacting with the 'profile' function in views.py. The function returns all survey objects (that have been created with the help of the 'Survey' model in models.py) in chronological order. The template displays all surveys, where the user id is the same as the author id of the survey.

##### New Survey.html
The 'new_survey.html' extends the layout.html and loads the static files (index.js and styles.css). In the block script a javascript function written in index.js is plugged into the template. The logged in user is able to create a new survey in the form (which uses textarea tags) that is situated in the block body of the template. She or he is bound to provide a question and at least two answers. By clicking the submit button, a the javascript function described above is called to check if the user provided the question and at least answers 1 and 2. If she or he did not, an alert is displayed to the user, instructing him to provide the necessary inputs. Once all necessary information is provided, the survey is created with the help of the dedicated function in views.py and the 'Survey' model provided in models.py.

##### All Surveys.html
The 'surveys.html' template extends the layout.html template to inherit the design and loads the static files. On this page, all active surveys are displayed in chronological order: the newest surveys are on top. Each survey is displayed in a unique box (which is made by defining a 'survey' class in styles.css) which makes it visibly easier for the user to differentiate between the surveys.
Each survey shows the number of votes which the survey currently has. Each user can only vote once for each survey. This is made sure by the model 'Vote' in models.py and the 'surveys' function in views.py. It is called when the 'all surveys' route is requested and provides all necessary info the the template to either show a submit button or the text 'You have already voted' if the user already voted on this survey. The author of the survey (and only she or he) is also able to close the survey.

##### Closed Survey.html
The closed survey or 'results.html' extends the layout.html and loads the static files. In the block body it displays the results of the surveys by using returned information if the results function in views.py. Once a survey author closes a survey is is no longer visible on the all'surveys' page and the user is automatically taken to the closed surveys page where all closed surveys are displayed along with their results in chronological order (newest survey first). Along with the results the user can also see how many total votes each survey has had.

#### Python files

##### models.py
The models.py file defines the SQL models that are used by the webapp.

The 'User' model is imported from django and defines what information is needed from a user (username, password etc.). It interacts with almost all function views.py and is primarily used in the login and the register functions in views.py.

The 'Survey' model references the user model with a foreign key and then has the following inputs.: qestion, 4 answers (of which two can be blank), a timestamp and archived. The question and answers are textfields, the timestamp uses the DateTimeField and archived is a BooleanField to determine of a sruvey has been closed/archioved by the author or not.

The 'Vote' model consists of a question and an answer, which are again TextFields and the user column which references to User model with a foreign key.

##### urls.py
The urls.py file contains all urlpatterns to the routes and templates. This is a django requirement which is mandatory for the webapp to be working properly. The routes and templates are linked to the respective functions in the vies.py file.

##### views.py
The views.py file in the polly (app) directory is the main file to contain python code and functions which interact with the form templates and return information to the templates to be displayed properly.
From django and datetime it imports various moduls, such as authenticate, render, datetime etc. which are used in the functions. It also imports all django models from models.py.

The index function simply returns the index template as explained above by requesting it.

The login function also takes only request as its sole input. If the method is 'POST, the login function tries to sign in the user by using the authenticate modul from django and by checking the user database on the data which is submitted by the user. If the credentials are faulty the function renders a message that is shown to the user. Otherwise, the user is logged in successfully.
If the request method is 'GET' the 'login.html' template is rendered.

The logout function uses the logout modul from django and logs the user out. It then uses HTTPResponseRedirect to render the index page.

The register function also interacts with the django user model. If the request method is 'POST' it tries to create a column in the user model with a new user. If the user typed in the corect credentials and the username is not already taken, the user is created in the user model; else, the user is prompted with a message, that either the passwords must match e.g. or that the username is already taken. If the request method is 'GET' the register template is simply displayed with its forms, so the user can start registering.

The new_survey function takes as input also only 'request'. If the request method is 'GET', the function simply returns and renders the new_survey.html for the user to create a new survey. If the request method is 'POST', the function accesses the values of the form on the new survey template and with creates a new Survey model with these values. Afterwards, the model is saved and the user is redirected to the 'all surveys' route.

The 'survey' also only takes 'request' as its sole input. If the requerst method is 'GET', the function accesses both the Survey model and the vote model to get access to their respective values. It then returns and renders the surveys.html template with all the information of the Survey and Vote model needed to display all the surveys in chronological order and all total votes of each survey. If the request method is 'POST' the function has two paths. If 'submit' is part of request.POST, the function accesses the values submitted on the template (question, user and answer) to create a Vote model, to ultimately keep track of the vote of the user on a specific survey. If 'close' is part of request.POST, the boolean field in the Survey model is accessed and changed to 'True'. The user is then redirected to the results template.

The 'profile' function also only takes 'request' as its sole input. It accesses all survey objects and returns them to the profile page in chronological order.

The results function also only takes 'request' as its sole input. It accesses all survey objects that have been archived. Also it acceses the values of the Vote objects. Afterwards an empty list is created. Then a for-loop over all archived surveys iterates over all archived surveys and calculates the answer rate in percentage for each answer. These results are appended to an empty dictionary in the for loop. Each iteration appends this dictionary to the empty list which has been created outsiode the for loop. The function ultimately returns the list with the dictionaries that contain the results of each archived survey. These reults are then displayed on the reults page.







