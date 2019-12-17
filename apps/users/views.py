from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from apps.users.forms import UserRegisterForm
from apps.users.models import User
from apps.verification.models import PhoneVerification


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            tenant = request.tenant
            form.instance.tenant = tenant
            form.save()
            user = User.objects.get(username=form.instance)
            user_count = User.objects.filter(tenant=tenant).count()
            team_leader = Group.objects.get(name='Team leader')
            if user_count > 1:
                form.instance.is_active = False
                manager = Group.objects.get(name='Manager')
                user.groups.add(manager)
            else:
                user.groups.add(team_leader)
            phone_verify = PhoneVerification.objects.create(user=user)
            phone_verify.save()
            form.save()
            messages.success(request, f'Your account has been created! Manager\'s '
                                      f'must be approved by team leaders before login.')
            return redirect('check-phone-verified')
    else:
        form = UserRegisterForm()
    return render(request, 'users/user_form.html', {'form': form})




