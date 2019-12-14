from django.http import HttpResponseRedirect
from django.shortcuts import render

from apps.clients.forms import ClientForm
from apps.clients.models import Client, Domain
from configs.settings import DEVELOPMENT


def register(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            Client(schema_name='public').activate()
            tenant = Client()
            tenant.schema_name = form.cleaned_data['last_name'].lower()
            tenant.name = form.cleaned_data['last_name'].lower()
            tenant.save()
            domain = Domain()
            if DEVELOPMENT:
                domain.domain = tenant.schema_name + '.localhost'
            else:
                domain.domain = tenant.schema_name + '.sportclipspayroll.com'
            domain.tenant = tenant
            domain.is_primary = False
            domain.save()
            if DEVELOPMENT:
                return HttpResponseRedirect('//' + domain.domain + ':8000/register')
            else:
                return HttpResponseRedirect('//' + domain.domain + '/register')
    else:
        form = ClientForm()
    return render(request, 'clients/registration.html', {'form': form})
