from django.urls import path
from rest_framework import routers

from ads import views

router = routers.SimpleRouter()
router.register('', views.CategoryView)

urlpatterns = [
    path('', views.AdsListView.as_view()),
    path('create/', views.AdsCreateView.as_view()),
    path('update/<int:pk>', views.AdsUpdateView.as_view()),
    path('<int:pk>', views.AdsDetailView.as_view()),
    path('delete/<int:pk>', views.AdsDeleteView.as_view()),
    path('upload/<int:pk>',views.AdImageUpload.as_view()),

]

urlpatterns += router.urls

