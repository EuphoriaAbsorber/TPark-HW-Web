from itertools import islice
from random import randrange
from django.core.management.base import BaseCommand, CommandError
from app.models import Profile, User, Question, Answer, Tag, LikeQuestion, LikeAnswer


class Command(BaseCommand):

    def handle(self, *args, **options):
        tagList = []
        tagCount = 1000
        for i in range(tagCount):
            tag = Tag(name = "tag" + f'{i}', questionsCount = 0)
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
                         rating = 0)
            q.save()
            
            for j in range(randrange(1, 6)):
                tag = tagList[randrange(0, tagCount)]
                q.tags.add(tag)
                
                tag.questionsCount += 1
                tag.save()
            q.save()
            questionList.append(q)
        #Question.objects.bulk_create(questionList, questionCount)

        answerList = []
        answerCount = 2000

        for i in range(answerCount):
            user = userList[randrange(0, userCount)]
            
            ans = Answer(text =  "Answer Text " + f" {i}",
                         author = user,
                         question  = questionList[randrange(0, questionCount)],
                         rating = 0)
                    
            answerList.append(ans)
        Answer.objects.bulk_create(answerList, answerCount)

        for u in userList:
            for q in questionList:
                rand = randrange(0,3) - 1
                if(rand != 0):
                    like = LikeQuestion(question = q, user = user, value = rand)
                    q.rating += rand
                    q.save()
                    like.save()

            for a in answerList:
                rand = randrange(0,3) - 1
                if(rand != 0):
                    like = LikeAnswer(answer = a, user = user, value = rand)
                    a.rating += rand
                    a.save()
                    like.save()

