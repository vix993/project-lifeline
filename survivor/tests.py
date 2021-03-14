from rest_framework.test import APITestCase
from rest_framework import status

from rest_framework.reverse import reverse as api_reverse

class HealthCheckAPITestCase(APITestCase):
    def test_health_check(self):
        url = api_reverse("api-survivor:health-check")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)