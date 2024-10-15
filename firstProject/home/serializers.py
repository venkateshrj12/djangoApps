from rest_framework import serializers
from home.models import Person
import re

class PeopleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Person
        # fields = ['name', 'age', ]
        # exclude = ['name', 'age',]
        fields = '__all__'
        depth = 1 # to include nested fields


    # def validate(self, data):
    #     if 'age' in data and data['age'] < 18:
    #         raise serializers.ValidationError({'age': 'should be greater than 18'})

    #     return data

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