from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from apps.invite.forms import InviteForm
from django.views.generic.edit import FormView


class InviteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'invite/invite_form.html'
    form_class = InviteForm
    success_url = reverse_lazy('invite')
    success_message = "An SMS invite has been sent."
    permission_required = ('clients.add_client',)
    permission_denied_message = 'User does not have permissions to invite users.'

    def get_initial(self):
        initial = super(InviteView, self).get_initial()
        team_leader = self.request.user.get_full_name()
        domain = self.request.tenant.get_primary_domain().domain
        initial['message'] = f'{team_leader} sent you an invite for Sportclips payroll automation. ' \
                             f'Please visit {domain}/register to register.'
        return initial

    def form_valid(self, form):
        form.send_sms()
        return super().form_valid(form)
