from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Task
from .serializers import TaskSerializer, RegisterSerializer
from .permissions import IsOwner


# User Registration API

class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# List and Create API

class TaskListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        tasks = Task.objects.filter(
            user=request.user
        )

        serializer = TaskSerializer(
            tasks, many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = TaskSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(user=request.user)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# Retrieve, Update and Delete API

class TaskDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsOwner
    ]

    def get_object(self, pk, user):

        try:
            return Task.objects.get(
                pk=pk,
                user=user
            )

        except Task.DoesNotExist:
            return None

    def get(self, request, pk):

        task = self.get_object(pk, request.user)

        if task is None:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, task)

        serializer = TaskSerializer(task)

        return Response(serializer.data)

    def put(self, request, pk):

        task = self.get_object(pk, request.user)

        if task is None:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, task)

        serializer = TaskSerializer(
            task,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):

        task = self.get_object(pk, request.user)

        if task is None:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, task)

        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        task = self.get_object(pk, request.user)

        if task is None:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, task)

        task.delete()

        return Response(
            {"message": "Task deleted successfully"},
            status=status.HTTP_200_OK
        )