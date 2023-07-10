# Final Project CS50 Web Capstone - Polly, a simple survey website

## General
In my final project for CS50 Web-Capstone, I created a web app called 'Polly - A simple survey website'.
The idea is, that a user can register for the website and is then able to create surveys, vote on surveys (on his or her own and surveys created by others) and close surveys to be able to see the results of the survey, once the author feels, that a sufficient quantity of votes are in.

The web app uses the django framework for web apps, as introduced in the CS50 Web course. The web app uses in total, three SQL models: the user model, a 'survey' model and a 'vote' model.

In total, there are 8 templates (including the layout.html) which include an index page, a login page, a 'new survey' page, a 'profile' page, a 'register' page, a 'results' page and a 'surveys' page.

The views.py file includes 8 distinct functions (index, login, logout, register, new_survey, surveys, profile, results) that call and render the templates with the needed information to display the correct data.

### Index Page
The index page shows a short introduction to the web app and how it works.

### Login Page
The login page can only be reached if no user is logged in. A link called 'login' in the navbar at the top, takes the user to the login route.

### Register Page
If the user does not have an account yet, she or he is able to create an account either by clicking on 'register' in the navbar or by clicking on 'register here' in the login route.

### Profile Page
The profile page shows all surveys the user created. The newest survey is displayed at the top.

### New Survey Page
The logged in user is able to create a new survey in the 'new survey' route. She or he is bound to provide a question and at least two answers. By clicking the submit button, a java script function is called to check if the user provided the question and at least answers 1 and 2. If she or he did not, an alert is displayed to the user, instructing him to provide the necessary inputs. Once all necessary information is provided, the survey is created with the model provided in models.py.

### All Surveys Page
On this page, all active surveys are displayed in chronological order: the newest surveys are on top. Each survey is displayed in a unique box which makes it visibly easier for the user to differentiate between the surveys.
Each survey shows the number of votes which the survey currently has. Each user can only vote once for each survey. This is made sure by the model 'Vote' in models.py. It is called when the 'all surveys' route is requested and provides all necessary info the the template to either show a submit button or the text 'You have already voted' if the user already voted on this survey. The author of the survey (and only she or he) is also able to close the survey.

### Closed Survey Page
Once a survey author closes a survey is is no longer visible on the all'surveys' page and the user is automatically taken to the closed surveys page where all closed surveys are displayed along with their results in chronological order (newest survey first). Along with the results the user can also see how many total votes each survey has had.

## Distinctiveness and Complexity
The 'Polly - A simple survey website' is distinct from the other projects in this course, because it does not have anything to do with a network or a mail client for example. The survey website uses other models, other functions in views.py, other CSS and bootstrap styling and other javascript as used in the other projects. Also it is more complex in the respect that calculations need to be made with respect to the votes of the users.