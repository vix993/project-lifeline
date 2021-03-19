from django.http import HttpResponse

from rest_framework import generics, serializers

from survivor.serializers import ReportsSerializer
from survivor.models import Survivor, Reports
from survivor.validators import Validation

from survivor.services.utils import make_set

class ReportsView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    serializer_class = ReportsSerializer
    def get_object(self):
        if not Reports.objects.all():
            Reports.objects.create(
                percentage_infected='', percentage_healthy='', average_water='', average_soup='',
                average_pouch='', average_ak47='', points_lost=''
            )
        infected = 0
        healthy = 0
        qs = Survivor.objects.all()
        qs1 = Reports.objects.first()
        lost_points = 0
        fiji_water = 0
        campbell_soup = 0
        first_aid_pouch = 0
        ak47 = 0
        for element in qs:
            if element.infected:
                infected_set = make_set(element.items)
                for key in infected_set:
                    lost_points = lost_points + (int(infected_set[key]) * int(Validation().price_dict[key]))
                    if key == 'Fiji Water':
                        fiji_water += int(infected_set[key])
                    if key == 'Campbell Soup':
                        campbell_soup += int(infected_set[key])
                    if key == 'First Aid Pouch':
                        first_aid_pouch += int(infected_set[key])
                    if key == 'AK47':
                        ak47 += int(infected_set[key])
                infected += 1
            else:
                healthy += 1
                healthy_set = make_set(element.items)
                for key in healthy_set:
                    if key == 'Fiji Water':
                        fiji_water += int(healthy_set[key])
                    if key == 'Campbell Soup':
                        campbell_soup += int(healthy_set[key])
                    if key == 'First Aid Pouch':
                        first_aid_pouch += int(healthy_set[key])
                    if key == 'AK47':
                        ak47 += int(healthy_set[key])
        survivor_count = infected + healthy
        qs1.percentage_infected = '{:.2f}%'.format((infected / survivor_count) * 100)
        qs1.percentage_healthy = '{:.2f}%'.format((healthy / survivor_count) * 100)
        qs1.average_water = '{:.2f} Fiji Waters per survivor.'.format(fiji_water / survivor_count)
        qs1.average_soup = '{:.2f} Campbell Soups per survivor.'.format(campbell_soup / survivor_count)
        qs1.average_pouch = '{:.2f} First Aid Pouches per survivor.'.format(first_aid_pouch / survivor_count)
        qs1.average_ak47 = "{:.2f} AK47's per survivor.".format(ak47 / survivor_count)
        qs1.points_lost = "{} points lost due to owner infection.".format(lost_points)
        qs1.save()
        return qs1