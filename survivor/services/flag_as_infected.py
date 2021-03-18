from survivor.models import Survivor, FlagAsInfected

def do_flag_as_infected(request):
    qs = FlagAsInfected.objects.\
        filter(flager_pk__exact=self.request.data['flager_pk']).\
        filter(flaged_pk__exact=self.request.data['flaged_pk'])
    to_increment = int(request.data['flaged_pk']) - 1
    if qs:
        raise serializers.ValidationError("We have already received your flag")
    survivor_obj = Survivor.objects.all()[to_increment]
    survivor_obj.infection_marks += 1
    if survivor_obj.infection_marks > 4:
        survivor_obj.infected = True
    survivor_obj.save()