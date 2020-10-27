from rest_framework.serializers import ModelSerializer

from client_requests.models import Client


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'id',
            'full_name',
            'phone'
        )
