from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from  . import views # used to import all views from this app
from account.views import me, signup # used to import a specific view from this app



urlpatterns = [
    # if all views are imported from views.py then use this
    # path('signup/', views.SignupView.as_view(), name='signup'), 

    # if specific view imported then use this
    path('signup/', signup, name='signup'), 
    path('me/', me, name='me'),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh_token'),

]