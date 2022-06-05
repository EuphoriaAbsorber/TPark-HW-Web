from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from app.models import *
from app.forms import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def paginate(objects_list, request, per_page = 5):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    res = paginator.get_page(page)
    return res

def index(request):
    questions = Question.objects.returnHot()
    q = paginate(questions, request)
    return render(request, "index.html", {"questions": q})

def question(request, id:int):
    q = Question.objects.get(id=id)
    ans = Answer.objects.filter(question_id=id)
    if request.method == "GET":
        answer_form = AnswerForm()
    if request.method == "POST":
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            text = answer_form.cleaned_data['text']
            a = Answer(text =  text, author = request.user, question  = q, rating = 0)
            a.save()
        answer_form.clean()
    return render(request, "question.html", {"question": q, "answers": ans, "form": answer_form})

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

def Login(request):
    if request.method == "GET":
        user_form = LoginForm()
    if request.method == "POST":
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            user = authenticate(request, **user_form.cleaned_data)
            if user:
                login(request, user)
                return redirect(reverse("index"))
    return render(request, "login.html", {"form": user_form})

def signup(request):
    if request.method == "GET":
        user_form = SignUpForm()
    if request.method == "POST":
        user_form = SignUpForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                p = Profile(user = user)
                p.save()
                return redirect(reverse("index"))
    return render(request, "signup.html", {"form": user_form})

@login_required(login_url = 'login')
def ask(request):
    if request.method == "GET":
        question_form = QuestionForm()
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            title = question_form.cleaned_data['title']
            text = question_form.cleaned_data['text']
            tags = question_form.cleaned_data['tags']
            q = Question(title=title, text=text, author=request.user, rating=0)
            q.save()
            for tag in tags:
                q.tags.add(tag)
                q.save()
            if q:
                return redirect(f"question/{q.id}")
    return render(request, "ask.html", {"form": question_form})

def settings(request):
    if request.method == "GET":
        user_form = SettingsForm(initial={"username": request.user.username, "email":request.user.email})
    if request.method == "POST":
        user_form = SettingsForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password0 = user_form.cleaned_data['password0']
            password = user_form.cleaned_data['password']
            email = user_form.cleaned_data['email']
            user1 = authenticate(username=request.user.username, password=password0)
            if user1:
                user = request.user
                user.username = username
                if len(password) > 0:
                    user.set_password(password)
                user.email = email
                user.save()
    return render(request, "settings.html", {"form": user_form})
