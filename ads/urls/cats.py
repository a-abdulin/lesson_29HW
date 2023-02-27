from django.urls import path

from ads import views

from rest_framework import routers

router = routers.SimpleRouter()
router.register('', views.CategoryView)

urlpatterns = [

]

urlpatterns += router.urls

# urlpatterns = [
#     path('', views.CategoryListView.as_view()),
#     path('<int:pk>', views.CategoryDetailView.as_view()),
#     path('create/', views.CategoryCreateView.as_view()),
#
# ]

