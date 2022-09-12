from django.urls import path
from .import views

urlpatterns = [
    path('register/', views.userregister.as_view()),
    path('login/', views.userlogin.as_view()),
    path('profile/',views.userprofile.as_view()),
    path('handle/',views.handlefiles.as_view())
]
