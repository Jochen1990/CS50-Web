from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
from django.db.models import Count


from .models import *

# Create your views here.
def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")
    
def new_survey(request):
    if request.method == "GET":
        return render(request, "new_survey.html")
    
    if request.method == "POST":
        
        survey = Survey.objects.create(
            user = request.user,
            question = request.POST['question'],
            answer1 = request.POST['answer1'],
            answer2 = request.POST['answer2'],
            answer3 = request.POST['answer3'],
            answer4 = request.POST['answer4'],
            timestamp = datetime.datetime.now()
        )
        
        survey.save()

        return HttpResponseRedirect(reverse(surveys))
    

def surveys(request):
    if request.method == 'GET':
        questions_all = Vote.objects.filter(user=request.user).values_list('question', flat=True)
        surveyss = Survey.objects.all().order_by('-timestamp')
        votes = Vote.objects.values('question').annotate(c=Count('question'))
        questions = Vote.objects.values_list('question', flat=True)
        print(surveyss)


        return render(request, "surveys.html", {
            'surveys': surveyss,
            'questions_all': questions_all,
            'votes': votes,
            'questions': questions
        })
    
    if request.method == 'POST':
        if 'submit' in request.POST:
            vote = Vote.objects.create(
                question = request.POST['submit'],
                user = request.user,
                answer = request.POST['radAnswer']
            )

            vote.save()

            return HttpResponseRedirect(reverse(surveys))
        
        if 'close' in request.POST:
            s = Survey.objects.get(id=request.POST['close'])
            s.archived=True
            s.save()

            return HttpResponseRedirect(reverse(results))


def profile(request):
    surveys = Survey.objects.all().order_by('-timestamp')
    return render(request, "profile.html", {
        'surveys': surveys
    })

def results(request):
        if request.method == 'GET':
            surveyss = Survey.objects.values().filter(archived=True)
            votes = Vote.objects.values('question').annotate(c=Count('question'))
            answers = list(Vote.objects.values_list('answer', flat=True))
            questions = Vote.objects.values_list('question', flat=True)
            print(votes)

            lists=[]
            
            for survey in surveyss:
                dict={}
                dict['question'] = survey['question']
                try:
                    total_counts = list(Vote.objects.values('question').filter(question=survey['question']).annotate(c=Count('question')))
                    total_counts = total_counts[0]['c']

                    
                    if survey['answer1'] in answers:
                        counts = answers.count(survey['answer1'])

                        ratio = "{:.0%}".format((counts / total_counts)) 
                        dict['answer1'] = survey['answer1'] + ': ' + ratio

                    elif survey['answer1'] not in answers:
                        dict['answer1'] = survey['answer1'] + ': 0%' 

                    if survey['answer2'] in answers:
                        counts = answers.count(survey['answer2'])

                        ratio = "{:.0%}".format((counts / total_counts)) 
                        dict['answer2'] = survey['answer2'] + ': ' + ratio

                    elif survey['answer2'] not in answers:
                        dict['answer2'] = survey['answer2'] + ': 0%'

                    if survey['answer3'] in answers:
                        counts = answers.count(survey['answer3'])

                        ratio = "{:.0%}".format((counts / total_counts)) 
                        dict['answer3'] = survey['answer3'] + ': ' + ratio

                    elif survey['answer3'] not in answers:
                        dict['answer3'] = survey['answer3'] + ': 0%'

                    if survey['answer4'] in answers:
                        counts = answers.count(survey['answer4'])
                        
                        ratio = "{:.0%}".format((counts / total_counts)) 
                        dict['answer4'] = survey['answer4'] + ': ' + ratio

                    elif survey['answer4'] not in answers:
                        dict['answer4'] = survey['answer4'] + ': 0%'

                 
          
                    lists.append(dict)

                except IndexError:
                    total_counts = 0

                    if survey['answer1'] in answers: 
                        dict['answer1'] = survey['answer1'] + ': 0%'

                    elif survey['answer1'] not in answers:
                        dict['answer1'] = survey['answer1'] + ': 0%' 

                    if survey['answer2'] in answers:
                        dict['answer2'] = survey['answer2'] + ': 0%'

                    elif survey['answer2'] not in answers:
                        dict['answer2'] = survey['answer2'] + ': 0%'

                    if survey['answer3'] in answers:
                        dict['answer3'] = survey['answer3'] + ': 0%'

                    elif survey['answer3'] not in answers:
                        dict['answer3'] = survey['answer3'] + ': 0%'

                    if survey['answer4'] in answers:
                        dict['answer4'] = survey['answer4'] + ': 0%'

                    elif survey['answer4'] not in answers:
                        dict['answer4'] = survey['answer4'] + ': 0%'

                    lists.append(dict)



           


            #iterate over all surveys that are archived:
                # append survey.question to empty dict
                    # if survey.answer1 in list of voted answers:
                        # count the occurence of this answer and divide it by the occurence of the question in votes
                        # append survey.answer1 and result to dict.
                    # else:
                        # append survey.answer1 with result of 0% to the dict
                    #repeat for answers 2-4

                ##--> then you have adict with survey.question, survey.answer1-4 xx%
                
            

            return render(request, "results.html", {
                'lists': lists,
                'votes': votes,
                'questions': questions
            })
        

