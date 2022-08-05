import json

import requests as requests
from django.shortcuts import render, HttpResponse

from .models import Greeting


# Create your views here.

def searchresult(request):
    try:
        rollno = request.GET["rollno"]
        d = {"status": "ok", "rollno": rollno, "result": "passed"}
        d = json.dumps(d)
        return HttpResponse(d)
    except:
        d = {"status": "error"}
        d = json.dumps(d)
        return HttpResponse(d)


def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def db(request):
    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


def apiquiz(request):
    answers = request.session.get("answers")
    if answers == None:
        answers = []
    qno = 0
    if qno == 0:
        try:
            request.session.pop("answers")
        except:
            pass
    p = ''
    response = requests.get(
        'https://gist.githubusercontent.com/champaksworldcreate/320e5af5ea9dbd31597d220637885587/raw/99f8f7a4df34ae477dcceb62598aa0bdde9ef685/tfquestions.json')
    data = response.json()
    data = data.get("questions")
    p = data[qno]["question"]
    # print(len(data))
    # print(data)
    if request.GET:
        option = int(request.GET["option"])
        if option == 1:
            option = "true"
        else:
            option = "false"

        correctanswer = data[qno].get("correctanswer")
        # print(option, correctanswer)
        iscorrect = option == correctanswer  # this will give us a boolean option

        answers.append(iscorrect)
        request.session["answers"] = answers
        print((iscorrect))
        qno = int(request.GET["qno"])
        qno += 1
        if qno >= len(data):
            return render(request, "result.html", {"answer": answers})
        p = data[qno]["question"]

    # print(p)
    return render(request, "apitest.html", {"data": p, "qnumber": qno + 1, "qno": qno})
