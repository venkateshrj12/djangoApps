from django.urls import path, re_path
from home.views import not_fuond, courses, people, person, login

urlpatterns = [
    path('courses/', courses),
    path('person/<int:id>', person),
    path('people/', people),
    path('login/', login),

    re_path(r'^.*$', not_fuond),
]