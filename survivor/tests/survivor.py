from rest_framework.test import APITestCase
from rest_framework import status

from rest_framework.reverse import reverse as api_reverse

from survivor.models import Survivor, FlagAsInfected, Reports

class SurvivorAPITestCase(APITestCase):
    def setUp(self):
        survivor = Survivor.objects.create(
            name='New Name', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652'
        )

    def test_single_post(self):
        post_count = Survivor.objects.count()
        self.assertEqual(post_count, 1)

    def test_get_list(self):
        data = {}
        url = api_reverse("api-survivor:create-list-survivors")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item(self):
        survivor = Survivor.objects.first()
        data = {"name": "New Second Test Name", "age": "20", "gender": "M",
                "latitude": "11", "longitude": "22",
                "items": "Fiji Water:100;Campbell Soup:200;First Aid Pouch:150;AK47:50"}
        url = api_reverse("api-survivor:create-list-survivors")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_item(self):
        survivor = Survivor.objects.first()
        data = {}
        url = survivor.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        survivor = Survivor.objects.first()
        url = survivor.get_api_url()
        data = {"age": "16", "latitude": "66677888", "longitude": "332222111"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_item_with_user(self):
        survivor = Survivor.objects.first()
        url = survivor.get_api_url()
        data = {"age": "16", "latitude": "66677888", "longitude": "332222111"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_latlon(self):
        survivor = Survivor.objects.first()
        url = survivor.get_api_url()
        data = {"latitude": "30", "longitude": "30"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item(self):
        data = {"name": "Third Test Name", "age": "20", "gender": "M",
                "latitude": "11", "longitude": "22",
                "items": "Fiji Water:1500;Campbell Soup:200;First Aid Pouch:150;AK47:50"}
        url = api_reverse("api-survivor:create-list-survivors")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        survivor = Survivor.objects.create(
            name='Usain Bolt',
            age='27',
            gender='M',
            latitude="77.232323",
            longitude="77.788888",
            items="Fiji Water:1500;Campbell Soup:200;First Aid Pouch:150;AK47:50",
        )
        url = survivor.get_api_url()
        data = {"latitude": "66", "longitude": "33"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)