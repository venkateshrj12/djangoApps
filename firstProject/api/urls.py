from django.urls import path, re_path, include
from home.views import not_fuond, courses, people, person, login, BookAPI, BookViewSet, RegisterUser

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='books')
urlpatterns = router.urls

urlpatterns = [
    # api view decorators
    path('courses/', courses),
    path('person/<int:id>', person),
    path('people/', people),
    path('login/', login),

    # API view class
    path('book/', BookAPI.as_view()),
    path('signup/', RegisterUser.as_view()),

    # API ViewSet Class
    path('', include(router.urls)),

    # Catch-all route for 404
    re_path(r'^.*$', not_fuond),
]