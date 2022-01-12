from django_filters.rest_framework import FilterSet, DateFromToRangeFilter

from advertisements.models import Advertisement


class AdvertisementFilter(FilterSet):
    created_at = DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['creator', 'status', 'created_at']
