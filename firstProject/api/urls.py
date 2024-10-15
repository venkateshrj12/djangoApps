from django.urls import path
from home.views import courses, people, person, login

urlpatterns = [
    path('courses/', courses),
    path('person/<int:id>', person),
    path('people/', people),
    path('login/', login),
]