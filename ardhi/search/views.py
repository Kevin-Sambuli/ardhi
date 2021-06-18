from django.http import HttpResponse, JsonResponse
from parcels.models import Parcels, ParcelDetails
from django.core.serializers import serialize
from django.core.mail import send_mail
from .models import PropertySearch
from django.conf import settings
from parcels.map import my_map
from .forms import SearchForm
import json


# Create your views here.
def search_view2(request):
    user = request.user.id
    context = {}
    if request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            owner = form.cleaned_data.get('owner')
            parcel_no = form.cleaned_data.get('parcel')
            purpose = form.cleaned_data.get('purpose')


            # sending the search details to the data base using orm
            # search = PropertySearch(owner=owner, parcel=parcel_no, purpose=purpose)
            # search.save()

            try:
                parcel = Parcels.objects.get(lr_no=parcel_no)
                pd = ParcelDetails.objects.get(parcel=Parcels.objects.get(lr_no=parcel_no))

                # generating parcels geojson to be displayed on the map
                parcel_as_geojson = serialize('geojson', Parcels.objects.all())
                parcel_data = serialize('geojson', Parcels.objects.filter(id=parcel_no))

                # saving the map to html
                map2 = my_map(parcel=parcel_data, land_parcels=parcel_as_geojson)
                map2.save('search/templates/parcels/parcel_search.html')

            
                # sending the email to the parcel owner in question
                # next it will be adding an stk push to the parcel search
                own = Parcels.objects.get(id=parcel_no)
                send_mail('Ardhi Parcel Search',
                    f'''Hey, {Ownership.objects.get(parcel=parcel).owner}, {request.user} 
                    has requested to view your land details, are you willing to allow him/her..?''',
                    settings.DEFAULT_FROM_EMAIL,
                    [Account.objects.get(id=own.owner_id).email],
                    fail_silently=False,)

                context['details'] = pd
                context['full_names'] = Ownership.objects.get(parcel=parcel).owner
                context['email'] = Account.objects.get(id=own.owner_id)

                return render(request, 'search/search_details.html', context)

            except DoesNotExist as e:
                return HttpResponse("The parcel you searched does not exist")
                # messages.success(request, f"Hey {request.user.username}, You have successfully been Registered..")

            # return redirect('search')
        else:
            context['search_form'] = form
    else:
        form = SearchForm()
        context['search_form'] = form
    return render(request, 'search/search.html', context)




def search_view(request):
    user = request.user.id

    # parcel_no= 'LR12872/84'
    parcel_no= 'LR12872/108'
    try:
        parcel = Parcels.objects.get(lr_no=parcel_no)
        print('parcel', parcel)
        pd = ParcelDetails.objects.get(parcel=Parcels.objects.get(lr_no=parcel_no))
        print('parcel details id', pd.parcel.id)
        print('parcel tenure', pd.tenure)
        print('parcel encumbrances', pd.encumbrances)
        print('parcel land use', pd.land_use) 

    except:
        print("DoesNotExist")
    

    # generating parcels geojson to be displayed on the map
    # parcel_as_geojson = serialize('geojson', Parcels.objects.all())
    # parcel_data = serialize('geojson', Parcels.objects.filter(lr_no=parcel_no))

    # saving the map to html
    # map2 = my_map(parcel=parcel_data, land_parcels=parcel_as_geojson)
    # map2.save('search/templates/search/parcelsearch2.html')
    finally:
        print('parcel printed')
    return HttpResponse('json')


