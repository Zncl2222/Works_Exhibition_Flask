from rest_framework import status
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import SgsimHistory
from .serializers import ParametersSerializer
from .serializers import SgsimListSerializer
from .serializers import SgsimSerializer
from .sgsim import get_cov_model
from utils.permissions import EmailVerify


class SgsimModelViewSet(viewsets.GenericViewSet, CreateModelMixin):
    queryset = SgsimHistory.objects.all()
    serializer_class = ParametersSerializer
    permission_classes = [IsAuthenticated, EmailVerify]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cov_model = get_cov_model(serializer.validated_data['cov_model'])
        data, run_time = cov_model(
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


class SgsimListViewSet(viewsets.ModelViewSet):
    queryset = SgsimHistory.objects.all()
    serializer_class = SgsimListSerializer
    permission_classes = [IsAuthenticated, EmailVerify]
