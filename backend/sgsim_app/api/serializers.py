from rest_framework import serializers

from ..models import Parameters_records
from ..models import Sgsim


class ParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameters_records
        fields = [
            'id',
            'realizations_number',
            'cov_model',
            'kernel',
            'bandwidth',
            'bandwidth_step',
            'x_size',
            'y_size',
            'randomseed',
            'krige_range',
            'krige_sill',
        ]


class SgsimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sgsim
        fields = '__all__'


class SgsimListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sgsim
        fields = ['create_date', 'results', 'run_time']

    def to_representation(self, instance):
        data = {}
        data['user'] = instance.user.username
        data.update(super().to_representation(instance))
        parameter = {}

        for attr, val in instance.parameters.__dict__.items():
            if type(val) in [int, float, str, dict]:
                parameter[attr] = val

        data['parameters'] = parameter

        return data
