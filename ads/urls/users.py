from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ads import views_users

urlpatterns = [
    path('', views_users.UserListView.as_view()),
    path('<int:pk>/', views_users.UserDetailView.as_view()),
    path('create/', views_users.UserCreateView.as_view()),
    path('update/<int:pk>', views_users.UserUpdateView.as_view()),
    path('delete/<int:pk>', views_users.UserDeleteView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

]