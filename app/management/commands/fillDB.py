from itertools import islice
from random import randrange
from django.core.management.base import BaseCommand, CommandError
from app.models import Profile, User, Question, Answer, Tag, LikeQuestion, LikeAnswer


class Command(BaseCommand):

    def handle(self, *args, **options):
        tagList = []
        tagCount = 1000
        for i in range(tagCount):
            tag = Tag(name = "tag" + f'{i}')
            tagList.append(tag)
        Tag.objects.bulk_create(tagList, tagCount)

        userList = []
        profileList = []
        userCount = 1000
        user = User(username = "admin")
        for i in range(userCount):
            user = User(username = "User" + f" {i+1}")
            prof = Profile(user = user)
            userList.append(user)
            profileList.append(prof)
        User.objects.bulk_create(userList, userCount)
        Profile.objects.bulk_create(profileList, userCount)

        questionList = []
        questionCount = 1000

        for i in range(questionCount):
            user = userList[randrange(0, userCount)]
            
            q = Question(
                         title = "Question " + f" {i+1}",
                         text =  "Question Text " + f" {i+1}",
                         author = user,
                         rating = randrange(-10000, 10000))
            q.save()
            for j in range(randrange(1, 6)):
                q.tags.add(tagList[randrange(0, tagCount)])
                q.save()

            questionList.append(q)
        #Question.objects.bulk_create(questionList, questionCount)

        answerList = []
        answerCount = 3000

        for i in range(answerCount):
            user = userList[randrange(0, userCount)]
            
            ans = Answer(text =  "Answer Text " + f" {i}",
                         author = user,
                         question  = questionList[randrange(0, questionCount)],
                         rating = randrange(-100, 100))
            answerList.append(ans)
        Answer.objects.bulk_create(answerList, answerCount)

