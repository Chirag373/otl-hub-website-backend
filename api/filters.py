import django_filters
from django.db.models import Q
from api.models import SellerProfile, PartnerProfile

class PropertyFilter(django_filters.FilterSet):
    keywords = django_filters.CharFilter(method='filter_keywords')
    location = django_filters.CharFilter(method='filter_location')
    price_min = django_filters.NumberFilter(field_name='estimated_value', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='estimated_value', lookup_expr='lte')
    beds = django_filters.NumberFilter(field_name='bedrooms', lookup_expr='gte')
    baths = django_filters.NumberFilter(field_name='bathrooms', lookup_expr='gte')
    type = django_filters.CharFilter(field_name='property_type', lookup_expr='iexact')
    zip_code = django_filters.CharFilter(field_name='zip_code', lookup_expr='icontains')

    class Meta:
        model = SellerProfile
        fields = ['type', 'beds', 'baths']

    def filter_keywords(self, queryset, name, value):
        return queryset.filter(
            Q(property_description__icontains=value) | 
            Q(city__icontains=value) |
            Q(street_address__icontains=value)
        )

    def filter_location(self, queryset, name, value):
        return queryset.filter(
            Q(city__icontains=value) | 
            Q(state__icontains=value) | 
            Q(zip_code__icontains=value)
        )


class PartnerFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    type = django_filters.CharFilter(field_name='partnership_type', lookup_expr='exact')

    class Meta:
        model = PartnerProfile
        fields = ['type']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(company_name__icontains=value) |
            Q(service_areas__icontains=value)
        )
