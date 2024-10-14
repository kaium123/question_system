# questions/urls.py

from django.urls import path
from .views import TagWithCountView, QuestionView, FavoriteQuestionView,ReadQuestionView,TagListView,QuestionListView,TagCreateView

urlpatterns = [
    path('tags-with-count/', TagWithCountView.as_view(), name='tag'),
    path('create-tag/', TagCreateView.as_view(), name='tag'),

    path('tags-with-question/', QuestionListView.as_view(), name='tag'),

    path('questions/', QuestionView.as_view(), name='question'),
    path('fav-questions/', FavoriteQuestionView.as_view(), name='fav-question'),
    path('read-questions/', ReadQuestionView.as_view(), name='read-question'),
    path('tags-list/', TagListView.as_view(), name='tag'),



]
