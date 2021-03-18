from rest_framework.test import APITestCase
from rest_framework import status

from rest_framework.reverse import reverse as api_reverse

from .models import Survivor, FlagAsInfected

class HealthCheckAPITestCase(APITestCase):
    def test_health_check(self):
        url = api_reverse("health-check")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

urltrade = api_reverse("api-survivor:trade-create")
class TradeItemAPITestCase(APITestCase):
    def setUp(self):
        survivor = Survivor.objects.create(
            name='New Name', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652'
        )
    def test_valid_trade_post(self):
        Survivor.objects.create(
            name='NEW NAME NAME', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652'
        )
        Survivor.objects.create(
            name='NEW NAME NAMEY NAME', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652'
        )
        data = {"buyer_pk": "1", "seller_pk": "2",
                "offered_items": "Fiji Water:2;Campbell Soup:0;First Aid Pouch:0;AK47:1",
                "requested_items": "Fiji Water:2;Campbell Soup:0;First Aid Pouch:0;AK47:1"}
        response = self.client.post(urltrade, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #print(response.data)
    def test_invalid_trade_insufficient_resource(self):
        Survivor.objects.create(
            name='NEW NAME NAME', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:0;Campbell Soup:0;First Aid Pouch:0;AK47:0'
        )
        Survivor.objects.create(
            name='NEW NAME NAMEY NAME', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:0;Campbell Soup:0;First Aid Pouch:0;AK47:0'
        )
        data = {"buyer_pk": "1", "seller_pk": "2",
                "offered_items": "Fiji Water:2;Campbell Soup:0;First Aid Pouch:0;AK47:1",
                "requested_items": "Fiji Water:0;Campbell Soup:0;First Aid Pouch:0;AK47:4"}
        response = self.client.post(urltrade, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        #print(response.data)
    def test_invalid_trade_with_infected(self):
        Survivor.objects.create(
            name='NEW NAME NAME', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652', infected=True
        )
        Survivor.objects.create(
            name='NEW NAME NAMEY NAME', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652'
        )
        data = {"buyer_pk": "1", "seller_pk": "2",
                "offered_items": "Fiji Water:2;Campbell Soup:0;First Aid Pouch:0;AK47:1",
                "requested_items": "Fiji Water:0;Campbell Soup:0;First Aid Pouch:0;AK47:4"}
        response = self.client.post(urltrade, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        #print(response.data)
    def test_uneven_trade_values(self):
        Survivor.objects.create(
            name='NEW NAME NAME', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652'
        )
        Survivor.objects.create(
            name='NEW NAME NAMEY NAME', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652'
        )
        data = {"buyer_pk": "1", "seller_pk": "2",
                "offered_items": "Fiji Water:1;Campbell Soup:0;First Aid Pouch:0;AK47:1",
                "requested_items": "Fiji Water:0;Campbell Soup:0;First Aid Pouch:0;AK47:4"}
        response = self.client.post(urltrade, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(response.data)
    def test_correct_trade_outcome(self):
        Survivor.objects.create(
            name='NEW NAME NAME', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652'
        )
        Survivor.objects.create(
            name='NEW NAME NAMEY NAME', age=20, gender='M', latitude='11', longitude='22',
            items='Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652'
        )
        data = {"buyer_pk": "1", "seller_pk": "2",
                "offered_items": "Fiji Water:5;Campbell Soup:0;First Aid Pouch:0;AK47:0",
                "requested_items": "Fiji Water:0;Campbell Soup:5;First Aid Pouch:1;AK47:0"}
        post_trade_data = 'Fiji Water:18;Campbell Soup:12;First Aid Pouch:17;AK47:652'
        post_trade_data_buyer = 'Fiji Water:8;Campbell Soup:22;First Aid Pouch:19;AK47:652'
        response = self.client.post(urltrade, data, format='json')
        self.assertEqual(Survivor.objects.all()[1].items, post_trade_data)
        self.assertEqual(Survivor.objects.all()[0].items, post_trade_data_buyer)
        print(response.data)
def test_incorrect_trade_outcome(self):
    Survivor.objects.create(
        name='NEW NAME NAME', age=20, gender='M', latitude='11', longitude='22',
        items='Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652'
    )
    Survivor.objects.create(
        name='NEW NAME NAMEY NAME', age=20, gender='M', latitude='11', longitude='22',
        items='Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652'
    )
    data = {"buyer_pk": "1", "seller_pk": "2",
            "offered_items": "Fiji Water:5;Campbell Soup:0;First Aid Pouch:0;AK47:0",
            "requested_items": "Fiji Water:0;Campbell Soup:6;First Aid Pouch:1;AK47:0"}
    post_trade_data = 'Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652'
    post_trade_data_buyer = 'Fiji Water:13;Campbell Soup:17;First Aid Pouch:18;AK47:652'
    response = self.client.post(urltrade, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(Survivor.objects.all()[1].items, post_trade_data)
    self.assertEqual(Survivor.objects.all()[0].items, post_trade_data_buyer)
    print(response.data)