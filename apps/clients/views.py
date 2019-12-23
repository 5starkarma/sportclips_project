from django.contrib.auth.models import Group, Permission
from django.http import HttpResponseRedirect
from django.shortcuts import render

from apps.clients.forms import ClientForm
from apps.clients.models import Client, Domain
from configs.permissions import team_leader_perms, manager_perms
from configs.settings import DEVELOPMENT


def tenant_register(request):
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
            team_leader, created = Group.objects.get_or_create(name='Team leader')
            for perm in team_leader_perms:
                permission = Permission.objects.get(codename=perm)
                team_leader.permissions.add(permission)
            manager, created = Group.objects.get_or_create(name='Manager')
            for perm in manager_perms:
                permission = Permission.objects.get(codename=perm)
                manager.permissions.add(permission)
            if DEVELOPMENT:
                return HttpResponseRedirect('//' + domain.domain + ':8000/register')
            else:
                return HttpResponseRedirect('//' + domain.domain + '/register')
    else:
        form = ClientForm()
    return render(request, 'clients/register.html', {'form': form})


def input_billing_info(request):
    return render(request, 'clients/checkout.html')
