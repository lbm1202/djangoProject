from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('',views.index, name='index'),
    path('add',views.add, name='add'),
    path('add/<int:exam_id>/problem',views.problem, name='problem'),
    path('<int:exam_id>/', views.detail, name='detail'),
     path('<int:exam_id>/statistic', views.statistic, name='statistic'),
    path('<int:exam_id>/results/', views.results, name='results'),
    path('<int:exam_id>/score/', views.score, name='score'),
    path('add/<int:exam_id>/problem/addProblem', views.addProblem, name='addProblem'),
]