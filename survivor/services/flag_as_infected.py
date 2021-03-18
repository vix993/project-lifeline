from survivor.models import Survivor, FlagAsInfected

from rest_framework.serializers import ValidationError

def do_flag_as_infected(request):
    qs = FlagAsInfected.objects.\
        filter(flager_pk__exact=request.data['flager_pk']).\
        filter(flaged_pk__exact=request.data['flaged_pk'])
    to_increment = int(request.data['flaged_pk']) - 1
    if qs:
        raise ValidationError("We have already received your flag")
    survivor_obj = Survivor.objects.all()[to_increment]
    survivor_obj.infection_marks += 1
    if survivor_obj.infection_marks > 4:
        survivor_obj.infected = True
    survivor_obj.save()