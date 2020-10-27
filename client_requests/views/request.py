from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.viewsets import ModelViewSet

from client_requests.serializers import (
    CreateRequestSerializer,
    RequestSerializer
)
from client_requests.models import Request


class RequestViewSet(ModelViewSet):
    serializer_class = CreateRequestSerializer
    queryset = Request.objects.select_related('responsible', 'client').all()

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return RequestSerializer
        return super(RequestViewSet, self).get_serializer_class()

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        return super(RequestViewSet, self).list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 5))
    def retrieve(self, request, *args, **kwargs):
        return super(RequestViewSet, self).retrieve(request, *args, **kwargs)
