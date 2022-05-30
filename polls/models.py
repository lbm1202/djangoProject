from django.db import models

# Create your models here.

class Exam(models.Model):
    exam_text = models.CharField(max_length=200)

    def __str__(self):
        return self.exam_text

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_contents = models.TextField()

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    answer = models.BooleanField(default = False)
    votes = models.IntegerField(default=0)


    def __str__(self):
        return self.choice_text


