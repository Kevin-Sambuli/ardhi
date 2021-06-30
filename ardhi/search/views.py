from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from parcels.models import Parcels, ParcelDetails
from django.core.serializers import serialize
from django.core.mail import send_mail
from accounts.models import Account
from .models import PropertySearch
from django.conf import settings
from parcels.map import my_map
from .forms import SearchForm
import json


# Create your views here.
def search_view(request):
    user_id = get_object_or_404(Account, id=request.user.id)
    context = {}
    if request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            parcel_no = form.cleaned_data.get('parcel')
            purpose = form.cleaned_data.get('purpose')
            try:
                parcel = Parcels.objects.get(lr_no=parcel_no)
                details = ParcelDetails.objects.get(parcel=Parcels.objects.get(lr_no=parcel_no))

                search = PropertySearch(owner=user_id, parcel=parcel_no, purpose=purpose)
                search.save()
            except:
                return HttpResponse("Am sorry the land parcel you are looking doesnt exist")

            context['owner'] = Account.objects.get(id=parcel.owner_id)
            context['parcel'] = parcel
            context['details'] = details

            points_as_geojson = serialize('geojson', Parcels.objects.all())
            parcel_json = serialize('geojson', Parcels.objects.filter(lr_no=parcel))
            print(parcel_json)
            m = my_map(land_parcels=points_as_geojson, parcel=parcel_json)
            m = m._repr_html_()
            context['map'] = m

            # send_mail('Ardhi Parcel Search',
            #           f'''Hey, {Account.objects.get(parcel=parcel).owner}, {request.user}
            #                     has requested to view your land details, are you willing to allow him/her..?''',
            #           settings.DEFAULT_FROM_EMAIL,
            #           [Account.objects.get(id=own.owner_id).email],
            #           fail_silently=False, )

            return render(request, 'search/search_details.html', context)
        else:
            context['search_form'] = form
    else:
        form = SearchForm()
        context['search_form'] = form
    return render(request, 'search/search.html', context)
