from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import  Choice,Question,Exam
from django.http import Http404


def index(request):
    latest_exam_list = Exam.objects.order_by()
    return render(request,'polls/index.html', {'latest_exam_list': latest_exam_list})

def statistic(request, exam_id):
    exam = get_object_or_404(Exam, pk= exam_id)
    static_list = []

    for question in exam.question_set.all():
        users = 0
        answer_num = 0
        for choice in question.choice_set.all():
            users += choice.votes
            if choice.answer == True:
                answer_num += choice.votes
        if(users == 0):
            users = 1
        
        static_list.append(round(answer_num/users*100, 2))
    return render(request,'polls/statistic.html',{'exam':exam, 'static_list': static_list})

def problem(request, exam_id):
    exam = get_object_or_404(Exam, pk= exam_id)
    return render(request,'polls/problem.html',{'exam':exam})

def addProblem(request, exam_id):
    try:
        Exam.objects.create(
            exam_text = request.POST['ename']
        )
        return HttpResponseRedirect(reverse('polls:add'))
    except:
        exam_now = get_object_or_404(Exam, pk= exam_id)
        if 'on' in request.POST.getlist('choice', ''):
            Question.objects.create(
                question_text = request.POST['qname'],
                question_contents = request.POST['qcontents'],
                exam = exam_now
            )
            condition = False
            for i in request.POST.getlist('choice', ''):
                if i == 'on':
                    condition = True
                else:
                    Choice.objects.create(
                        choice_text = i,
                        answer = condition,
                        votes = 0,
                        question = Question.objects.order_by('-pk')[0]
                    )
                    condition = False
        else:
            return render(request, 'polls/problem.html',{'exam':exam_now,'error_message':'Fail to save Problem. There must be at least one answer'})
    else:
        pass
    return HttpResponseRedirect(reverse('polls:index'))

def add(request):
    latest_exam_list = Exam.objects.order_by()
    return render(request,'polls/add.html',{'latest_exam_list': latest_exam_list})

def detail(request, exam_id):
    exam = get_object_or_404(Exam, pk= exam_id)

    return render(request, 'polls/detail.html',{'exam':exam})

def results(request, exam_id, score):
    exam = get_object_or_404(Exam, pk= exam_id)

    return render(request, 'polls/results.html',{'exam':exam ,'score':score})


def score(request, exam_id):
    exam = get_object_or_404(Exam, pk= exam_id)
    selected_choices = []
    score = 0
    num = 0
    try:
        for question in exam.question_set.all():
            selected_choices.append(question.choice_set.get(pk=request.POST[question.question_text])) 
            num += 1
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'exam': exam,'error_message': "You didn't select a choice.",})
    else:
        for i in selected_choices:
            i.votes += 1
            i.save()
            if i.answer == True:
                score += 100/num
        return render(request,'polls/results.html',{'exam': exam, 'score':round(score,2)} )