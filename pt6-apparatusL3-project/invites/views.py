from django.http import HttpResponseRedirect, request
from django.views.generic import TemplateView, FormView, UpdateView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from apparatusl3.decorators import has_permissions
from .models import Meeting, MeetingInvites
from .forms import MeetingsScheduleForm
from l3meetings.models import MeetingAgenda
    
    
@method_decorator(has_permissions(['invites.change_meetinginvites']), name='dispatch')
class UpdateInvite(LoginRequiredMixin, UpdateView):
    model = MeetingInvites
    form_class = MeetingsScheduleForm
    template_name = 'create.html'
    success_url = reverse_lazy('meetings_list')
    login_url = "/login/"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def get_object(self):
        meeting_id = self.kwargs.get('pk')
        invite = get_object_or_404(MeetingInvites, meeting__id=meeting_id)
        return invite
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Meeting Invite'
        return context
    
    def form_valid(self, form):
        try:
            form.save()
            messages.success(self.request, 'Meeting invite updated successfully.')
        except Exception as e:
            messages.error(self.request, 'There was an error updating the invite.')
            return self.form_invalid(form)
        return super().form_valid(form)


@method_decorator(has_permissions(['invites.delete_meetinginvites']), name='dispatch')
class DeleteSchedule(LoginRequiredMixin, View):
    success_url = reverse_lazy('invites:invite_list')

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(MeetingInvites, pk=kwargs['pk'])
        obj.delete()
        messages.success(request, 'The invite was deleted successfully.')
        return HttpResponseRedirect(self.success_url)
    