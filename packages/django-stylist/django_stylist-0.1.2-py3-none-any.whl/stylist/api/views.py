from rest_framework.generics import CreateAPIView
from django.contrib.sites.models import Site
from django.shortcuts import redirect

from stylist.models import Style 
from stylist.api.serializers import StyleSerializer


class StyleCreateAPIView(CreateAPIView):
     queryset = Style.objects.all()
     serializer_class = StyleSerializer

     def perform_create(self, serializer):
          site = Site.objects.get_current()
          instance = serializer.save(site=site)
          instance.compile_attrs()

          if not Style.objects.filter(site=site, enabled=True):
               instance.enabled = True
               instance.save()

     def create(self, request, *args, **kwargs):
          response = super().create(request, *args, **kwargs)
          return redirect('stylist:stylist-index')
