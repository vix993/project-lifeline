from rest_framework.test import APITestCase
from rest_framework import status

from rest_framework.reverse import reverse as api_reverse

from survivor.models import Survivor, FlagAsInfected, Reports

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