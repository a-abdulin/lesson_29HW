from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, UpdateView
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ads.models import Category, ADS, Location, Selection
from ads.permissions.ad import IsADOwner
from ads.permissions.selection import IsOwner
from ads.serializers import CategorySerializer, ADSSerializer, LocationSerializer, SelectionSerializer
from dj_project import settings


def root(request):
    return JsonResponse({
        "status": "ok"
    })

@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class LocationView(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]


class AdsListView(ListView):
    queryset = ADS.objects.all()
    serializer_class = ADSSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by('-price')

        cat_ids = request.GET.getlist("cat", [])
        if cat_ids:
            if not self.object_list.filter(category_id__in=cat_ids):
                return JsonResponse({"error": "No cat_id", "status": 200})
            self.object_list = self.object_list.filter(category_id__in=cat_ids)

        text = request.GET.get("text", None)
        if text:
            if not self.object_list.filter(name__icontains=text):
                return JsonResponse({"error": "No adds for text", "status": 200})
            self.object_list = self.object_list.filter(name__icontains=text)

        location = request.GET.get("location", None)
        if location:
            if not self.object_list.filter(author_id__location_id__name__icontains=location):
                return JsonResponse({"error": "No adds for location", "status": 200})
            self.object_list = self.object_list.filter(author_id__location_id__name__icontains=location)

        price_from = request.GET.get("price_from", None)
        price_to = request.GET.get("price_to", None)
        price_q = None
        if price_from and not price_to:
            price_q = Q(price__gte=int(price_from))
        elif not price_from and price_to:
            price_q = Q(price__lte=int(price_to))
        elif price_from and price_to:
            price_q = Q(price__gte=int(price_from)) & Q(price__lte=int(price_to))
        if price_q:
            self.object_list = self.object_list.filter(price_q)


        page = int(request.GET.get("page", 0))
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_obj = paginator.get_page(page)

        response = []
        response.append({
            "totals": paginator.count,
            "num_page": paginator.num_pages,
            "items": ADSSerializer(page_obj, many=True).data
        })

        return JsonResponse(response, safe=False)


class AdsCreateView(generics.CreateAPIView):
    queryset = ADS.objects.all()
    serializer_class = ADSSerializer


class AdsUpdateView(generics.UpdateAPIView):
    queryset = ADS.objects.all()
    serializer_class = ADSSerializer
    permission_classes = [IsAuthenticated, IsADOwner]


class AdsDeleteView(generics.DestroyAPIView):
    queryset = ADS.objects.all()
    serializer_class = ADSSerializer
    permission_classes = [IsAuthenticated, IsADOwner]


class AdsDetailView(generics.RetrieveAPIView):
    queryset = ADS.objects.all()
    serializer_class = ADSSerializer
    permission_classes = [IsAuthenticated]


class AdImageUpload(UpdateView):
    model = ADS
    fields = ["name", "author_id", "price", "description", "is_published"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get("image")
        self.object.save()

        return JsonResponse({"name": self.object.name, "image": self.object.image.url})


class SelectionCreateView(generics.CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated]

class SelectionListView(generics.ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated]


class SelectionUpdateView(generics.UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class SelectionDetailedView(generics.RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated]


class SelectionDeleteView(generics.DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, IsOwner]

