import pytest

from .models import (
    Employee,
    Client,
    Request
)


@pytest.fixture
def create_employee():
    def create(full_name, position):
        return Employee.objects.create(full_name=full_name, position=position)
    return create


@pytest.fixture
def create_client():
    def create(full_name, phone):
        return Client.objects.create(full_name=full_name, phone=phone)
    return create


@pytest.fixture
def create_request():
    def create(text, client, employee):
        return Request.objects.create(text=text,
                                      responsible=employee,
                                      client=client)
    return create

