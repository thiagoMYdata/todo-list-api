from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

class TaskNotDoneListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["title", "description"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]
