from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Task
from .serializers import TaskSerializer, UserSerializer, TaskNotDoneListSerializer


@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response({"detail": "not found."}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})


@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST", "GET", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def apiTaskCRUD(request):
    if request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"It worked!", "task":serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    elif request.method == "GET": 
        task = Task.objects.filter(is_task_done=False, owner=request.user.username).order_by("-create_at")
        serializer = TaskNotDoneListSerializer(task, many=True)
        return Response(serializer.data)

    elif request.method == "PATCH":
        task = get_object_or_404(Task.objects.filter(id=request.data["id"]), owner=request.user.username)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "UPDATED!", "task": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    elif request.method == "DELETE": 
        task = get_object_or_404(Task.objects.filter(id=request.data["id"]), owner=request.user.username)
        serializer = TaskSerializer(task)
        task.delete()
        return Response({"message":"DELETED", "deleted_task":serializer.data})
