from rest_framework.test import APITestCase
from rest_framework import status

from rest_framework.reverse import reverse as api_reverse

from survivor.models import Survivor, FlagAsInfected, Reports

class ReportsAPITestCase(APITestCase):
    def setUp(self):
        Survivor.objects.create(
            name='New Name', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652'
        )
        Survivor.objects.create(
            name='New Name', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652'
        )
    def test_report_get(self):
        url = api_reverse("api-survivor:reports-retrieve-update")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        Survivor.objects.create(
            name='New Name FHEUHF', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:27;Campbell Soup:40;First Aid Pouch:18;AK47:652'
        )
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        Survivor.objects.create(
            name='New Name FHEUHFddwdw', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:0;Campbell Soup:0;First Aid Pouch:0;AK47:300', infected=True
        )
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)