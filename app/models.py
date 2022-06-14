from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    avatar = models.ImageField(blank=True)
    def __str__(self):
        return f"{self.user.username}"

class QuestionManager(models.Manager):
    def FilterByTag(self, newTag):
        return self.filter(tags = newTag.id)

    def returnBest(self):
        return self.order_by('-rating')

    def returnHot(self):
        return self.order_by('-release_date')

class TagManager(models.Manager):
    def filterByQuestionCount(self):
        return self.order_by('-questionsCount')

class Tag(models.Model):
    name = models.CharField(max_length = 40)
    questionsCount = models.IntegerField(default=0)

    objects = TagManager()

    def __str__(self):
        return f"{self.name}"

class Question(models.Model):
    title = models.CharField(max_length = 40)
    tags = models.ManyToManyField(Tag, blank=True)
    text = models.TextField(max_length = 1000)
    author = models.ForeignKey(User, models.PROTECT)
    release_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(blank=True, null=True)

    objects = QuestionManager()

    def __str__(self):
        return f"{self.title}"

    def rateIncrease(self):
        self.rating += 1
        self.save()

    def rateDecrease(self):
        self.rating -= 1
        self.save()

    def getTags(self):
        return self.tags

class AnswerManager(models.Manager):
    def filterByRate(self):
        return self.order_by('-rating')

class Answer(models.Model):
    text = models.TextField(max_length = 1000)
    author = models.ForeignKey(User, models.PROTECT)
    question = models.ForeignKey(Question, models.CASCADE)
    release_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(blank=True, null=True)
    isCorrect = models.BooleanField(blank=True, null=True)

    objects = AnswerManager()

    def __str__(self):
        return f"{self.author}'s answer"

    def rateIncrease(self):
        self.rating += 1
        self.save()

    def rateDecrease(self):
        self.rating -= 1
        self.save()

    def changeCorrectState(self):
        self.isCorrect = not(self.isCorrect)
        self.save()

class LikeQuestion(models.Model):
    question = models.ForeignKey(Question, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)
    value = models.IntegerField(default=0)

class LikeAnswer(models.Model):
    answer = models.ForeignKey(Answer, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)
    value = models.IntegerField(default=0)