from rest_framework import status
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Sgsim
from .serializers import ParametersSerializer
from .serializers import SgsimListSerializer
from .serializers import SgsimSerializer
from .sgsim import sgsim_gaussian


class SgsimModelViewSet(viewsets.GenericViewSet, CreateModelMixin):
    queryset = Sgsim.objects.all()
    serializer_class = ParametersSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data['cov_model'] == 'Gaussian':
            data, run_time = sgsim_gaussian(
                serializer.validated_data,
            ).run_sgsim()
        else:
            data, run_time = sgsim_gaussian(
                serializer.validated_data,
            ).run_sgsim()
        parameters = serializer.save()

        sgsim_data = {}
        sgsim_data['results'] = data
        sgsim_data['run_time'] = run_time
        sgsim_data['parameters'] = parameters.id
        sgsim_data['user'] = request.user.id
        self.serializer_class = SgsimSerializer
        serializer = self.get_serializer(data=sgsim_data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(data, status=status.HTTP_201_CREATED)


class SgsimListViewSet(viewsets.ModelViewSet):
    queryset = Sgsim.objects.all()
    serializer_class = SgsimListSerializer
    permission_classes = [IsAuthenticated]
