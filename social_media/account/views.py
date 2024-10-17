import pdb
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView

from .serializers import SignupSerializer

@api_view(['GET'])
def me(request):
    user = request.user
    return JsonResponse(SignupSerializer(user).data)
    
@api_view(['POST'])
@permission_classes([]) # nullifying permission validation
@authentication_classes([]) # nullifying authentication validation
def signup(request):
    data = request.data
    message = 'Sucess'
    serializer = SignupSerializer(data = data)
    
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'status': message,  'data': serializer.data}, status=200)

    return JsonResponse({'errors': serializer.errors})
