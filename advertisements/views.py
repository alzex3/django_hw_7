from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import IsOwnerOrAdmin
from .models import Advertisement


class AdvertisementViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = AdvertisementFilter

    def get_queryset(self):
        if self.action == 'list':
            user = self.request.user
            public_query = Q(status="OPEN") | Q(status="CLOSED")
            private_query = public_query | Q(creator_id=user.id)

            if user.is_staff:
                return self.queryset

            elif user.is_authenticated:
                return self.queryset.filter(private_query)

            else:
                return self.queryset.filter(public_query)

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        return []
