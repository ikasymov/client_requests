from rest_framework import serializers


from client_requests.models import Request

from .client import ClientSerializer
from .employee import EmployeeSerializer


class CreateRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = (
            'text',
            'responsible',
            'client'
        )


class RequestSerializer(serializers.ModelSerializer):
    responsible = EmployeeSerializer(read_only=True)
    client = ClientSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Request
        fields = (
            'id',
            'text',
            'created_at',
            'responsible',
            'client'
        )
