from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from django.core.cache import cache
from app.models import *
from app.forms import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.defaults import page_not_found


def paginate(objects_list, request, per_page = 5):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    res = paginator.get_page(page)
    return res

def handler404(request):
    return HttpResponse(status = 404)

def index(request):
    questions = Question.objects.returnHot()
    q = paginate(questions, request)
    tags = Tag.objects.filterByQuestionCount()[:10]
    return render(request, "index.html", {"questions": q, "tags": tags})

def question(request, id:int):
    try:
        q = Question.objects.get(id=id)
        ans = Answer.objects.filter(question_id=id)
        tags = Tag.objects.filterByQuestionCount()[:10]
        if request.method == "GET":
            answer_form = AnswerForm()
        if request.method == "POST":
            answer_form = AnswerForm(request.POST)
            if answer_form.is_valid():
                text = answer_form.cleaned_data['text']
                a = Answer(text =  text, author = request.user, question  = q, rating = 0)
                a.save()
            answer_form.clean()
    except:
        return HttpResponse(status = 404)
    
    return render(request, "question.html", {"question": q, "answers": ans, "form": answer_form, "tags": tags})

def hot(request):
    questions = Question.objects.returnBest()
    q = paginate(questions, request)
    tags = Tag.objects.filterByQuestionCount()[:10]
    return render(request, "hot.html", {"questions": q, "tags": tags})

def tag(request, s:str):
    try:
        newTag = Tag.objects.get(name = s)
    except:
        return HttpResponse(status = 404)
    questions = Question.objects.FilterByTag(newTag)
    tags = Tag.objects.filterByQuestionCount()[:10]
    q = paginate(questions, request)
    return render(request, "tag.html", {"questions": q, "tag": newTag.name, "tags": tags})

def Login(request):
    tags = Tag.objects.filterByQuestionCount()[:10]
    if request.method == "GET":
        user_form = LoginForm()
        cache.set('next', request.GET.get('next', None))
    if request.method == "POST":
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            user = authenticate(request, **user_form.cleaned_data)
            if user:
                login(request, user)
                next_url = cache.get('next')
                if next_url:
                    cache.delete('next')
                    return redirect(next_url)
                return redirect(reverse("index"))
    return render(request, "login.html", {"form": user_form, "tags": tags})

def signup(request):
    tags = Tag.objects.filterByQuestionCount()[:10]
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
    return render(request, "signup.html", {"form": user_form, "tags": tags})

@login_required(login_url = 'login')
def ask(request):
    poptags = Tag.objects.filterByQuestionCount()[:10]
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

            tagList = []

            for tag in tags:
                try:
                    t = Tag.objects.get(name = tag)
                except:
                    t = Tag(name = tag, questionsCount = 0)
                    t.save()
                t.questionsCount += 1
                t.save()
                tagList.append(t)
                
            for tag in tagList:
                q.tags.add(tag)
            q.save()

            if q:
                return redirect(f"question/{q.id}")
    return render(request, "ask.html", {"form": question_form, "tags": poptags})

@login_required(login_url = 'login')
def settings(request):
    tags = Tag.objects.filterByQuestionCount()[:10]
    if request.method == "GET":
        user_form = SettingsForm(initial={"username": request.user.username, "email":request.user.email, "avatar": request.user.profile.avatar})
    if request.method == "POST":
        user_form = SettingsForm(request.POST, files = request.FILES, instance = request.user.profile, initial={"username": request.user.username, "email":request.user.email, "avatar": request.user.profile.avatar})
        if user_form.is_valid():
            password0 = user_form.cleaned_data['password0']
            password = user_form.cleaned_data['password']
            user1 = authenticate(username=request.user.username, password=password0)
            if user1:
                user = request.user
                if len(password) > 0:
                    user.set_password(password)
                    user.save()
                user_form.saveAvatar()
                return redirect(reverse("settings"))
    return render(request, "settings.html", {"form": user_form, "tags": tags})

@login_required(login_url = 'login')
def likes(request):
    question_id = request.POST["question_id"]
    like_type = request.POST["like_type"]
    try:
        q = Question.objects.get(id=question_id)
        # try:
        #     like = LikeQuestion.objects.filter(question__pk=question_id).get(user=request.user)
        #     value = like.value
        #     like.delete()
        #     q.updateRating((-1)*value)
        # except:
        like = LikeQuestion.objects.create(user=request.user, question=q, value=int(like_type))
        like.save()
        q.updateRating(like.value)
        return JsonResponse({"new_rating":q.rating})
    except:
        return JsonResponse({"error_code":404})

@login_required(login_url = 'login')
def markAnswer(request):
    question_id = request.POST["question_id"]
    answer_id = request.POST["answer_id"]
    try:
        q = Question.objects.get(id=question_id)
        a = Answer.objects.get(id=answer_id)
        if q.author.id == request.user.id:
            a.isCorrect = not a.isCorrect
            a.save()
            return JsonResponse({"is_correct":answer_id})
        else:
            return JsonResponse({"error_code":403})
    except:
        return JsonResponse({"error_code":404})