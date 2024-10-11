from home.views import courses
from django.urls import path

urlpatterns = {
    path('courses/', courses),
}