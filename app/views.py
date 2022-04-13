from django.shortcuts import render

QUESTIONS = [
    {
        "title": f"Question {i}",
        "text": f"Q Text {i}",
        "id": i,
    } for i in range(10)
]

ANSWERS = [
    {
        "title": f"ANSWER {i}",
        "text": f" A Text {i}",
    } for i in range(10)
]


def index(request):
    return render(request, "index.html", {"questions": QUESTIONS})

def ask(request):
    return render(request, "ask.html", {"questions": QUESTIONS})

def question(request, id:int):
    return render(request, "question.html", {"question": QUESTIONS[id], "answers": ANSWERS})

def login(request):
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")

def hot(request):
    return render(request, "hot.html", {"questions": QUESTIONS})

def tag(request, s:str):
    return render(request, "tag.html", {"questions": QUESTIONS})