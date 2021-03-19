from rest_framework.test import APITestCase
from rest_framework import status

from rest_framework.reverse import reverse as api_reverse

from survivor.models import Survivor, FlagAsInfected, Reports

class FlagAsInfectedAPITestCase(APITestCase):
    def setUp(self):
        Survivor.objects.create(
            name='New Name', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652'
        )
        FlagAsInfected.objects.create(
            flager_pk='1', flaged_pk='2'
        )
    def test_flag_post(self):
        Survivor.objects.create(
            name='NAME NAME NMAME', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652', infection_marks='4'
        )
        Survivor.objects.create(
            name='NAME NAME NAMEY NAME', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652', infection_marks='4'
        )
        url = api_reverse("api-survivor:flag-create")
        data = {"flaged_pk": "1", "flager_pk": "2"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Unable to repeat flags of the same details
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test whether infected is updating
        data = {"flaged_pk": "2", "flager_pk": "3"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Survivor.objects.all()[1].infected, True)