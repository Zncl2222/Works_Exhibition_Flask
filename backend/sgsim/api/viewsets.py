from rest_framework import status
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters import rest_framework as filters

from ..models import SgsimHistory
from .filters import SgsimHistoryFilter
from .paginations import SgsimListPagination
from .serializers import ParametersSerializer
from .serializers import SgsimListSerializer
from .serializers import SgsimSerializer
from .sgsim import Sgsim
from utils.permissions import EmailVerify


class SgsimModelViewSet(viewsets.GenericViewSet, CreateModelMixin, ListModelMixin):
    queryset = SgsimHistory.objects.all()
    serializer_class = ParametersSerializer
    pagination_class = SgsimListPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SgsimHistoryFilter
    permission_classes = [IsAuthenticated, EmailVerify]

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_class
        elif self.action == 'list':
            return SgsimListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data, run_time = Sgsim(
            data=serializer.validated_data,
        ).run_sgsim()

        parameters = serializer.save()

        sgsim_data = {}
        sgsim_data['results'] = data
        sgsim_data['run_time'] = run_time
        sgsim_data['parameters'] = parameters.id
        sgsim_data['user'] = request.user.id
        serializer = SgsimSerializer(data=sgsim_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data, status=status.HTTP_201_CREATED)
