from ..models import SgsimHistory
from django_filters import rest_framework as filters


class SgsimHistoryFilter(filters.FilterSet):
    class Meta:
        model = SgsimHistory
        fields = ['user', 'create_date', 'run_time']
