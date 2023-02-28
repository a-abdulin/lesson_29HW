
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics

from ads.models import User
from ads.serializers import UserSerializer, UserListSerializer, UserCUDSerializer


@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@method_decorator(csrf_exempt, name='dispatch')
class UserListView(generics.ListAPIView):
    queryset = User.objects.annotate(t_ads=Count("ads", filter=Q(ads__is_published=True))).order_by("username")
    serializer_class = UserListSerializer


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCUDSerializer


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCUDSerializer


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserCUDSerializer

