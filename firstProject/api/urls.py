from django.urls import path, re_path
from home.views import not_fuond, courses, people, person, login, BookAPI

urlpatterns = [
    # api view decorators
    path('courses/', courses),
    path('person/<int:id>', person),
    path('people/', people),
    path('login/', login),

    # API view class
    path('books/', BookAPI.as_view()),

    # Catch-all route for 404
    re_path(r'^.*$', not_fuond),
]