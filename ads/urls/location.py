from rest_framework import routers

from ads import views

router = routers.SimpleRouter()
router.register('', views.LocationView)

urlpatterns = [

]

urlpatterns += router.urls
