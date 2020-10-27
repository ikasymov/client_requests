from rest_framework.serializers import ModelSerializer

from client_requests.models import Employee


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id',
            'full_name',
            'position'
        )
