import django_filters
from django_filters import rest_framework as filters

from ..models import SgsimHistory


class SgsimHistoryFilter(filters.FilterSet):
    realizations_number = django_filters.RangeFilter(field_name='parameters__realizations_number')
    cov_model = django_filters.CharFilter(field_name='parameters__cov_model')
    kernel = django_filters.CharFilter(field_name='parameters__kernel')
    bandwidth = django_filters.RangeFilter(field_name='parameters__bandwidth')
    bandwidth_step = django_filters.RangeFilter(field_name='parameters__bandwidth_step')
    x_size = django_filters.RangeFilter(field_name='parameters__x_size')
    y_size = django_filters.RangeFilter(field_name='parameters__y_size')
    randomseed = django_filters.RangeFilter(field_name='parameters__randomseed')
    krige_range = django_filters.RangeFilter(field_name='parameters__krige_range')
    krige_sill = django_filters.RangeFilter(field_name='parameters__krige_sill')
    user = django_filters.CharFilter(field_name='user__username')
    create_date = django_filters.DateFromToRangeFilter(field_name='create_date')
    run_time = django_filters.RangeFilter(field_name='run_time')

    class Meta:
        model = SgsimHistory
        exclude = ['results']
