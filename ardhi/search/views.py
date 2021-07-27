from django.shortcuts import render, get_object_or_404
from parcels.models import Parcels, ParcelDetails
from django.core.serializers import serialize
from django.core.mail import send_mail
from django.http import HttpResponse
from accounts.models import Account
from .models import PropertySearch
from django.conf import settings
from parcels.map import my_map
from .forms import SearchForm
import json

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


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
                # search.save()
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


def render_pdf_view(request):
    template_path = 'user_printer.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response,)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# def hello(request):
#     today = datetime.datetime.now().date()
#
#     daysOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
#     return render(request, "hello.html", {"today": today, "days_of_week": daysOfWeek})
#
#
# The
# template
# to
# display
# that
# list
# using
# {{ for}} −
#
# < html >
# < body >
#
# Hello
# World!!! < p > Today is {{today}} < / p >
# We
# are
# { % if today.day == 1 %}
#
# the
# first
# day
# of
# month.
# { % elif today.day == 30 %}
#
# the
# last
# day
# of
# month.
# { % else %}
#
# I
# don
# 't know.
# { % endif %}
#
# < p >
# { %
# for day in days_of_week %}
# {{day}}
# < / p >
#
# { % endfor %}
#
# < / body >