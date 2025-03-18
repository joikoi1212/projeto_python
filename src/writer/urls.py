from django.urls import path 
from .views import dashboard
from . import views
urlpatterns = [
    path('dashboard/', dashboard, name='writer-dashboard'),
    path('create-article/', views.create_article, name='create-article'),
    path('my-article/', views.my_articles, name='my-articles'),
    path('update-article/<int:id>/', views.update_articles, name='update-article'),
    path('delete-article/<int:id>/', views.delete_article, name='delete-article'),
    path('update-user/', views.update_user, name='update-writer'), 
    path('delete-user/', views.delete_user, name='delete-user'), 
]