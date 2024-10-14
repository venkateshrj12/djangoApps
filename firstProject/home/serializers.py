from rest_framework import serializers
from home.models import Person

class PeopleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Person
        # fields = ['name', 'age', ]
        # exclude = ['name', 'age',]
        fields = '__all__'