from django.http import HttpResponse

from rest_framework import generics, serializers

from survivor.models import Survivor, Reports

from survivor.validators import Validation
from survivor.services.utils import make_set

# Class will fetch all survivor info and tally the items
# We separate the ones owned by healthy and infected survivors
# Then tally the value and quantity of each to form our report

class ReportService:
    def do_report(self):
        qs, qs1 = self.get_data_and_get_or_create_report()
        
        report_features = {
            'infected': 0, 'healthy': 0, 'lost_points': 0,
            'Fiji Water': 0, 'Campbell Soup': 0, 'First Aid Pouch': 0,
            'AK47': 0}
        for element in qs:
            if element.infected:
                infected_set = make_set(element.items)
                report_features = self.tally_infected_items(report_features, infected_set)
            else:
                healthy_set = make_set(element.items)
                report_features = self.tally_healthy_items(report_features, healthy_set)
        self.save_final_report(report_features, qs1)
    
    def get_data_and_get_or_create_report(self):
        if not Reports.objects.all():
                Reports.objects.create(
                    percentage_infected='', percentage_healthy='', average_water='', average_soup='',
                    average_pouch='', average_ak47='', points_lost=''
                )
        qs = Survivor.objects.all()
        qs1 = Reports.objects.first()
        return (qs, qs1)
    
    def tally_infected_items(self, report_features, infected_set):
        for key in infected_set:
            report_features['lost_points'] = report_features['lost_points'] + (int(infected_set[key]) * int(Validation().price_dict[key]))
            report_features['Fiji Water'] += int(infected_set['Fiji Water'])
            report_features['Campbell Soup'] += int(infected_set['Campbell Soup'])
            report_features['First Aid Pouch'] += int(infected_set['First Aid Pouch'])
            report_features['AK47'] += int(infected_set['AK47'])
        report_features['infected'] += 1
        return report_features
    
    def tally_healthy_items(self, report_features, healthy_set):
        report_features['healthy'] += 1
        for key in healthy_set:
            report_features['Fiji Water'] += int(healthy_set['Fiji Water'])
            report_features['Campbell Soup'] += int(healthy_set['Campbell Soup'])
            report_features['First Aid Pouch'] += int(healthy_set['Campbell Soup'])
            report_features['AK47'] += int(healthy_set['AK47'])
        return report_features
    
    def save_final_report(self, report_features, report_object):
        survivor_count = report_features['infected'] + report_features['healthy']
        report_object.percentage_infected = '{:.2f}%'.format((report_features['infected'] / survivor_count) * 100)
        report_object.percentage_healthy = '{:.2f}%'.format((report_features['healthy'] / survivor_count) * 100)
        report_object.average_water = '{:.2f} Fiji Waters per survivor.'.format(report_features['Fiji Water'] / survivor_count)
        report_object.average_soup = '{:.2f} Campbell Soups per survivor.'.format(report_features['Campbell Soup'] / survivor_count)
        report_object.average_pouch = '{:.2f} First Aid Pouches per survivor.'.format(report_features['First Aid Pouch'] / survivor_count)
        report_object.average_ak47 = "{:.2f} AK47's per survivor.".format(report_features['AK47'] / survivor_count)
        report_object.points_lost = "{} points lost due to owner infection.".format(report_features['lost_points'])
        report_object.save()