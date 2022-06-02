from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import *
from django.http import HttpResponse

# QUESTIONS = [
#     {
#         "title": f"Question {i}",
#         "text": f"Q Text {i}",
#         "id": i,
#     } for i in range(25)
# ]

# ANSWERS = [
#     {
#         "title": f"ANSWER {i}",
#         "text": f" A Text {i}",
#     } for i in range(10)
# ]

def paginate(objects_list, request, per_page = 5):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    res = paginator.get_page(page)
    return res


# def index(request):
#     return render(request, "index.html", {"questions": QUESTIONS})

def index(request):
    questions = Question.objects.returnHot()
    q = paginate(questions, request)
    return render(request, "index.html", {"questions": q})

def ask(request):
    return render(request, "ask.html")

def question(request, id:int):
    q = Question.objects.get(id=id)
    ans = Answer.objects.filter(question_id=id)
    return render(request, "question.html", {"question": q, "answers": ans})

def login(request):
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")

def hot(request):
    questions = Question.objects.returnBest()
    q = paginate(questions, request)
    return render(request, "hot.html", {"questions": q})

def tag(request, s:str):
    try:
        newTag = Tag.objects.get(name = s)
    except:
        return HttpResponse(status = 404)
    questions = Question.objects.FilterByTag(newTag)
    q = paginate(questions, request)
    return render(request, "tag.html", {"questions": q, "tag": newTag.name})