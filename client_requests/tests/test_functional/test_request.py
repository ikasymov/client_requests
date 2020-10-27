import pytest
from django.test import Client
from django.urls import reverse

from client_requests.models import Request

CLIENT_FULL_NAME = 'Test Client Full Name'
CLIENT_PHONE = '+71111111111'
EMPLOYEE_FULL_NAME = 'Test Employee Full Name'
EMPLOYEE_POSITION = 'position'
TEST_TEXT = 'test'


@pytest.mark.django_db(transaction=True)
def test_create_request(create_client,
                        create_employee):
    client_object = create_client(CLIENT_FULL_NAME,
                                  CLIENT_PHONE)
    employee_object = create_employee(EMPLOYEE_FULL_NAME,
                                      EMPLOYEE_POSITION)
    client = Client()
    url = reverse('requests-list')
    data = dict(responsible=employee_object.id,
                client=client_object.id,
                text=TEST_TEXT)
    res = client.post(url, data=data, content_type='application/json')

    request_object = Request.objects.last()
    expected_data = {
        "text": TEST_TEXT,
        "responsible": employee_object.id,
        "client": client_object.id
    }

    assert request_object.text == TEST_TEXT
    assert request_object.responsible.id == employee_object.id
    assert request_object.client.id == client_object.id
    assert res.json() == expected_data


@pytest.mark.django_db(transaction=True)
def test_list_request(create_client,
                      create_employee,
                      create_request):
    client_object = create_client(CLIENT_FULL_NAME,
                                  CLIENT_PHONE)
    employee_object = create_employee(EMPLOYEE_FULL_NAME,
                                      EMPLOYEE_POSITION)
    request_object = create_request(TEST_TEXT, client_object, employee_object)

    client = Client()
    url = reverse('requests-list')

    res = client.get(url)

    expected_data = [{
        'id': request_object.id,
        "text": TEST_TEXT,
        "created_at": request_object.created_at.strftime("%Y-%m-%d %H:%M"),
        "responsible": {
            "id": employee_object.id,
            "full_name": employee_object.full_name,
            "position": employee_object.position
        },
        "client": {
            "id": client_object.id,
            "full_name": client_object.full_name,
            "phone": client_object.phone
        }
    }]

    assert res.json() == expected_data


@pytest.mark.django_db(transaction=True)
def test_update_request(create_client,
                        create_employee,
                        create_request):
    client_object = create_client(CLIENT_FULL_NAME,
                                  CLIENT_PHONE)
    employee_object = create_employee(EMPLOYEE_FULL_NAME,
                                      EMPLOYEE_POSITION)
    request_object = create_request(TEST_TEXT, client_object, employee_object)

    client = Client()
    url = reverse('requests-detail', kwargs={'pk': request_object.id})
    new_text = TEST_TEXT + 'updated'

    data = dict(responsible=employee_object.id,
                client=client_object.id,
                text=new_text)

    res = client.put(url, data=data, content_type='application/json')

    expected_data = {
        "text": TEST_TEXT + 'updated',
        "responsible": employee_object.id,
        "client": client_object.id
    }
    assert res.json() == expected_data
    assert TEST_TEXT + 'updated' == Request.objects.get(
        id=request_object.id).text


@pytest.mark.django_db(transaction=True)
def test_delete_request(create_client,
                        create_employee,
                        create_request):
    client_object = create_client(CLIENT_FULL_NAME,
                                  CLIENT_PHONE)
    employee_object = create_employee(EMPLOYEE_FULL_NAME,
                                      EMPLOYEE_POSITION)
    request_object = create_request(TEST_TEXT, client_object, employee_object)

    client = Client()
    url = reverse('requests-detail', kwargs={'pk': request_object.id})

    res = client.delete(url)

    assert res.status_code == 204
    with pytest.raises(Request.DoesNotExist):
        Request.objects.get(id=request_object.id)
