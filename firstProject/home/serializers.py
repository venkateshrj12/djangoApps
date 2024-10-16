from rest_framework import serializers
from home.models import Person, Color, Book
from django.contrib.auth.models import User
import re
import pdb

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']

class PeopleSerializer(serializers.ModelSerializer):
    color = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all(), required= False)
    greetings = serializers.SerializerMethodField()

    class Meta:
        model = Person
        # fields = ['name', 'age', ]
        # exclude = ['name', 'age',]
        fields = '__all__'
        # depth = 1 # to include nested fields

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['color'] = ColorSerializer(instance.color).data if response['color'] else None
        return response

    def get_greetings(self, instance):
        return f'Hello, {instance.name}!'

# validations for serializers
    # def validate(self, data):
    #     if 'age' in data and data['age'] < 18:
    #         raise serializers.ValidationError({'age': 'should be greater than 18'})

    #     return data
    # Add this method to return full color details in the response

    def validate_age(self, age):
        if age < 18:
            raise serializers.ValidationError( 'Age should be greater than 18' )

        return age

    def validate_name(self, name):
        if len(name) < 3:
            raise serializers.ValidationError('Name should be greater than 3 characters')
        if not re.match("^[a-zA-Z0-9 ]*$", name):
            raise serializers.ValidationError('Name should not contain special characters')
        
        return name
    
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True) # if we use write_only = True, it will not be included in the response

    def validate(self, data):
        username = data.get('username', '')
        email = data.get('email', '')
        password = data['password']

        if User.objects.filter(username = username).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})

        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError({'email': "Email has been taken"})

        if len(password) < 8:
            raise serializers.ValidationError({'password': 'Password should be greater than 8 characters'})
        
        return data

    # def validate_uesrname(self, username):
    #     if User.objects.filter(username = username).exists():
    #         raise serializers.ValidationError('Username already exists')
    #     return username
        
    # def validate_email(self, email):
    #     if User.objects.filter(email = email).exists():
    #         raise serializers.ValidationError("Email has been taken")
    #     return email
    
    # def  validate_password(self, password):
    #     if len(password) < 8:
    #         raise serializers.ValidationError('Password should be greater than 8 characters')
    #     return password

    def create(self, validated_data):
        username = validated_data.get('username', '')
        email = validated_data.get('email', '')
        password = validated_data['password']

        # user = User.objects.create(
        #     username = username,
        #     email = email,
        #     password = password
        # ) #  this will create a new user in the database without password

        user = User.objects.create(
            username = username,
            email = email
        )
        user.set_password(password) # if we use set_password(password) method, it will hash the password
        user.save()

        return user

