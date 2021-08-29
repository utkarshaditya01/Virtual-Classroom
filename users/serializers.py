from rest_framework import serializers
from .models import Student, Tutor


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'username']


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['first_name', 'last_name', 'email', 'username']
