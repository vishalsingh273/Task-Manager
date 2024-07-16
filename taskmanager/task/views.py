from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Task
from .serializers import TaskSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

class TaskMemberView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, user_id):
        task = Task.objects.get(pk=pk)
        user = User.objects.get(pk=user_id)
        task.members.add(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk, user_id):
        task = Task.objects.get(pk=pk)
        user = User.objects.get(pk=user_id)
        task.members.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        members = task.members.all()
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data)

class UpdateTaskStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.status = request.data.get('status', task.status)
        task.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
