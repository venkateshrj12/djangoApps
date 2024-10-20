from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger


from home.models import Person, Book
from home.serializers import * # PeopleSerializer, LoginSerializer, BookSerializer, RegisterUserSerializer
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
        username = serializer.data['username']
        password = serializer.data['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'user': RegisterUserSerializer(user).data, 'token': str(token)})
        else:
            return Response({'errors': ['Invalid Credentials']}, status.HTTP_422_UNPROCESSABLE_ENTITY)

    return Response(serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def not_fuond(request):
    return Response('Page not found', status=status.HTTP_404_NOT_FOUND)

class BookAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        current_user = request.user
        objs = Book.objects.all()

        # Get page_number and handle ValueError
        try:
            page_number = int(request.GET.get('page_number', 1))
        except ValueError:
            page_number = 1
        
        # Get page_size and handle ValueError
        try:
            page_size = int(request.GET.get('page_size', 20))
        except ValueError:
            page_size = 20

        paginator = Paginator(objs, page_size)

        try:
            books = paginator.page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            books = paginator.page(1)
        except EmptyPage:
            # If page is out of range, return an empty list.
            books = []

        serializer = BookSerializer(books, many=True)
        return Response({
            'data': serializer.data, 
            'current_user': str(current_user),
            'total_pages': paginator.num_pages,
            'current_page': page_number
        })
    
    def post(self, request):
        data = request.data
        serializer = BookSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def patch(self, request):
        data = request.data
        book = get_object_or_404(Book, id = data['id'])
        serializer = BookSerializer(book, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def put(self, request):
        data = request.data
        book = get_object_or_404(Book, id = data['id'])
        serializer = BookSerializer(book, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request):
        id = request.data['data']
        book  = get_object_or_404(Book, id = id)
        book.delete()
        return Response({'message': 'success'})
    
class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def list(self, request):
        search = request.GET.get('search', '')
    
        queryset = self.queryset.filter(name__icontains=search) if search else self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        queryset = self.queryset
        book = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(book)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def search(self, request):
        query = request.GET.get('query', '')
    
        queryset = self.queryset.filter(name__icontains=query) if query else self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'])
    def publish(self, request,  pk=None):
        book = self.get_object()
        book.published = True
        book.save()
        serializer = self.serializer_class(book)
        return Response(serializer.data)




class RegisterUser(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterUserSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)