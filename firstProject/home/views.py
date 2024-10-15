from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from home.models import Person
from home.serializers import PeopleSerializer, LoginSerializer
import pdb

@api_view(['GET', 'POST', 'PATCH'])
def courses(request):
    courses = {
        'course_name': 'Python',
        'learn': ['flask', 'django']
    }
    if request.method == 'GET':
        name = request.GET.get('name')
        response = {'message': 'You hit GET request',
                    'courses': courses,
                     'name': name }
    elif request.method == 'POST':
        data = request.data
        response = {'message': 'You hit POST request',
                    'data': data }
    elif request.method == 'PATCH':
        data = request.data
        response = {'message': 'You hit Patch request',
                    'data': data }

    return Response(response)

@api_view(['GET', 'POST', 'DELETE'])
def people(request):
    if request.method == 'GET':
        # objs = Person.objects.all()
        objs = Person.objects.filter(color__isnull = False) # filtering the values based on color selection

        serializer = PeopleSerializer(objs, many = True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    else:
        id = request.data['id']
        obj = get_object_or_404(Person, id = id)
        obj.delete()
        return Response({'message': 'success'}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def  person(request, id):
    data = request.data
    obj = get_object_or_404(Person, id=id)
    if request.method == 'GET':
        serializer = PeopleSerializer(obj)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PeopleSerializer(obj, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = PeopleSerializer(obj, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        obj.delete()
        return Response({'message': 'success'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data = data)
    if serializer.is_valid():
        return Response({'message': 'success'})

    return Response(serializer.errors)