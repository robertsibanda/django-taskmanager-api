from django.urls import path
from . import views
urlpatterns = [
    path('', views.task_list_create),
    path('signup', views.signup),
    path('login', views.login),
    path('delete/<int:pk>', views.task_delete),
    path('update/<int:pk>', views.task_update)
]
