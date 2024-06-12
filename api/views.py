from rest_framework import authentication, generics, permissions, status
from rest_framework.response import Response
from tasks.models import Task
from tasks.serializers import TaskSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404


@api_view(["POST"])
def login(request, *args, **kwargs):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"error": "user not found"})

    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})


@api_view(["POST"])
def signup(request, *args, **kwargs):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user)
        return Response({"token": token})


class TaskListCreateView(generics.ListCreateAPIView):
    # retrieve all tasks or create a new one
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


task_list_create = TaskListCreateView.as_view()


class TaskUpdate(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = "pk"

    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if serializer.user == self.request.user:
            serializer.save()
        else:
            return Response({"error": "user cannot perform action"})


task_update = TaskUpdate.as_view()


class TaskDelete(generics.DestroyAPIView):
    # delete already created task
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = "pk"
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
        else:
            return Response({"error": "user cannot perform action"})


task_delete = TaskDelete.as_view()
