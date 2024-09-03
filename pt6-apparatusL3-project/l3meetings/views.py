from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView, FormView, UpdateView, View, ListView
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist
from .utils import UserUtils
from apparatusl3.decorators import has_permissions, has_role
from .models import *
from .forms import *
from django.db.models.signals import post_save
from .signals import meeting_saved
from django.contrib.auth.models import Group
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from pytz import timezone as tz
from django.db.models import Count, F
from sitesettings.email_notifications import *
from sitesettings.context_processors import get_holiday_dates
from sitesettings.context_processors import load_site_settings

local_tz = tz('Asia/Kolkata')
@method_decorator(has_permissions(['l3meetings.view_meeting']), name='dispatch')
class MeetingIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'meetings/index.html'
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Actions'
        context['meetings'] = Meeting.objects.all().order_by('-id')
        return context

@method_decorator(has_permissions(['l3meetings.view_meeting']), name='dispatch')
class MeetingDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'meetings/single.html'
    login_url = "/login/"
    
    def get(self, request, *args, **kwargs):
        request.session['origin_url'] = request.path
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(load_site_settings(self.request))
        meeting = Meeting.objects.get(slug=self.kwargs['slug'])
        context['page_title'] = 'Actions'
        context['meeting'] = meeting
        context['agendas'] = Agenda.objects.filter(meetingagenda__meeting=meeting).order_by("-is_default")
        context['action_items'] = ActionItem.objects.filter(meeting=meeting).order_by('-id')
        action_items = ActionItem.objects.filter(meeting=meeting).order_by('-id')
        unique_actions = {}

        for item in action_items:
            if item.title not in unique_actions:
                user = User.objects.get(id=item.assignedto_id)
                unique_actions[item.title] = {
                    'id': item.id,
                    'title': item.title,
                    'assignedto': {
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    },
                    'author_id': item.author_id,
                    'agenda_id': item.agenda_id,
                    'count': 1,
                }
            else:
                unique_actions[item.title]['count'] += 1

        context['action_items'] =  list(unique_actions.values())
        context['action_item_form'] = ActionItemForm(initial={'assignedto': self.request.user})
        meeting_notes, created = MeetingNotes.objects.get_or_create(meeting=meeting)
        context['meeting_notes_form'] = MeetingNotesForm(instance=meeting_notes)
        context['meeting_attendance_form'] = MeetingAttendanceForm(meeting=meeting)
        return context

    def get_success_url(self):
        origin_url = self.request.session.get('origin_url')
        del self.request.session['origin_url']
        return origin_url

    def post(self, request, *args, **kwargs):
        is_email_sending_allowed = self.get_context_data()['allow_email_send']
        
        match self.request.POST.get('form_name'):
            case 'add_agenda':
                try:
                    title = self.request.POST.get('agenda_title')
                    status = self.request.POST.get('status')
                    meeting_id = self.request.POST.get('meeting_id')
                    meeting = Meeting.objects.get(id=meeting_id)

                    agenda = Agenda(title=title, status=status,
                                    created_by=request.user)

                    agenda.save()
                    MeetingAgenda.objects.create(meeting=meeting, agenda=agenda)
                    # meeting_saved.send(sender=Meeting, instance=self.object, created=True, user=self.request.user)
                    messages.success(self.request, 'Agenda Created successfully.')
                except Exception as e:
                    print(e)
                    messages.error(self.request, 'There was an error creating the agenda.')
                return redirect(self.get_success_url())  
            
            case 'add_action_item':
                try:
                    assignedto = self.request.POST.get('assignedto')
                    title = self.request.POST.get('title')
                    meeting_id = self.request.POST.get('meeting_id')
                    agenda_id = self.request.POST.get('agenda_id')
                    meeting = Meeting.objects.get(id=meeting_id)
                    agenda = Agenda.objects.get(id=agenda_id)
                    user = User.objects.get(id=assignedto)
                    start_date = datetime.date.today()
                    target_end_date = start_date + datetime.timedelta(days=7)
                    superUsr = User.objects.filter(pk=assignedto, is_superuser=True).values()
                    
                    all_users =  User.objects.filter(is_superuser=False)

                    if superUsr:
                        action_items_for_all = [
                            ActionItem(assignedto=usereach, meeting=meeting,title=title,start_date=start_date,target_end_date=target_end_date,agenda=agenda,author=self.request.user)
                            for usereach in all_users
                        ]
                        ActionItem.objects.bulk_create(action_items_for_all)
                    else:
                        actionitem = ActionItem(assignedto=user,meeting=meeting,title=title,start_date=start_date,target_end_date=target_end_date,agenda=agenda,author=self.request.user)
                        actionitem.save()
                        if actionitem.assignedto:
                            if is_email_sending_allowed == '1':
                                send_action_item_notification_email(actionitem,'create')
                
                    messages.success(self.request, 'Action Item Created successfully.')

                except Exception as e:
                    print(e)
                    messages.error(self.request, 'There was an error creating the action item.')
                return redirect(self.get_success_url())
            
            case 'add_meeting_note':
                self.handle_add_meeting_note(request)
            
            case 'add_meeting_attendance':
                self.handle_add_meeting_attendance(request)
                
        return redirect(self.get_success_url())
          

    def handle_add_meeting_note(self, request):
        meeting = get_object_or_404(Meeting, slug=self.kwargs['slug'])
        meeting_notes, created = MeetingNotes.objects.get_or_create(meeting=meeting)
        meeting_notes_form = MeetingNotesForm(request.POST, instance=meeting_notes)
        if meeting_notes_form.is_valid():
            meeting_notes = meeting_notes_form.save(commit=False)
            meeting_notes.meeting = meeting
            meeting_notes.save()
            messages.success(request, 'Meeting Note Updated successfully.')
        else:
            messages.error(request, 'There was an error adding the Meeting Note.')
            
    def handle_add_meeting_attendance(self, request):
        meeting = get_object_or_404(Meeting, slug=self.kwargs['slug'])
        absent_users = self.request.POST.get('absent_users', '').split(',')
        present_users = self.request.POST.get('present_users', '').split(',')
        
        absent_users = [user_id.strip() for user_id in absent_users if user_id.strip()]
        present_users = [user_id.strip() for user_id in present_users if user_id.strip()]

        for user_id in absent_users:
            try:
                user = User.objects.get(id=user_id)
                MeetingAttendance.objects.update_or_create(
                    meeting=meeting,
                    user=user,
                    defaults={'is_present': False}
                )
            except User.DoesNotExist:
                print(f'User with ID {user_id} does not exist.')

        for user_id in present_users:
            try:
                user = User.objects.get(id=user_id)
                MeetingAttendance.objects.update_or_create(
                    meeting=meeting,
                    user=user,
                    defaults={'is_present': True}
                )
            except User.DoesNotExist:
                print(f'User with ID {user_id} does not exist.')
        messages.success(request, 'Meeting attendance updated successfully.')

@method_decorator(has_permissions(['l3meetings.change_agenda']), name='dispatch')
class UpdateAgenda(LoginRequiredMixin, UpdateView):
    def post(self, request, *args, **kwargs):
        try:
            title = request.POST.get('agenda_title')
            agenda_id = request.POST.get('agenda_id')
            status = request.POST.get('status')

            if not title or not agenda_id or not status:
                return JsonResponse({'success': False, 'message': 'Missing required fields'}, status=400)

            try:
                agenda = Agenda.objects.get(id=agenda_id)
            except ObjectDoesNotExist:
                return JsonResponse({'success': False, 'message': 'Agenda not found'}, status=404)

            agenda.title = title
            agenda.status = status
            agenda.save()

            return JsonResponse({'success': True, 'message': 'Agenda updated successfully'})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

@method_decorator(has_permissions(['l3meetings.add_meeting']), name='dispatch')
class CreateMeeting(LoginRequiredMixin, FormView):
    template_name = 'meetings/create.html'
    form_class = MeetingForm
    success_url = reverse_lazy('meetings_list')
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(load_site_settings(self.request))
        context['page_title'] = 'Create Meeting'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(CreateMeeting, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        context_data = load_site_settings(self.request)
        kwargs['context_data'] = {
            'default_meeting_title': context_data.get('default_meeting_title', '')
        }
        return kwargs
    
    def form_valid(self, form):
        try:
            meeting_date = form.cleaned_data.get('meeting_date')
            if meeting_date.weekday() >= 5:  # Saturday is 5 and Sunday is 6
                messages.error(self.request, "Meetings cannot be scheduled for weekends (Saturday or Sunday).")
                return self.form_invalid(form)

            meeting = form.save(commit=False)
            delivery_unit = form.cleaned_data.get('delivery_unit')
            default_agenda = DeliveryUnitDefaultAgenda.objects.filter(
                delivery_unit=delivery_unit)

            with transaction.atomic():
                meeting.save()
                if default_agenda.exists():
                    meeting_agendas = [
                        MeetingAgenda(meeting=meeting, agenda=item.agenda)
                        for item in default_agenda
                    ]
                    MeetingAgenda.objects.bulk_create(meeting_agendas)
                
                MeetingNotes.objects.create(meeting=meeting, note_description='None')

                meeting_saved.send(sender=Meeting, instance=meeting, created=True)
                messages.success(self.request, 'Meeting Created successfully.')
                assigned_user = form.cleaned_data.get('assigned_to')
                if assigned_user:
                    participant_group = Group.objects.get(name='Participant')
                    moderator_group = Group.objects.get(name='Moderator')

                    if assigned_user.groups.filter(name='Participant').exists():
                        assigned_user.groups.remove(participant_group)
                        assigned_user.groups.add(moderator_group)

            return redirect(self.get_success_url())

        except Agenda.DoesNotExist:
            messages.error(self.request, 'One or more agenda items do not exist.')
            return self.form_invalid(form)
        except Exception as e:
            print(f"Unexpected error: {e}")
            messages.error(self.request, 'There was an error creating the meeting.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

@method_decorator(has_permissions(['l3meetings.change_meeting']), name='dispatch')
class UpdateMeeting(LoginRequiredMixin, UpdateView):
    model = Meeting
    form_class = MeetingForm
    template_name = 'meetings/edit.html'
    success_url = reverse_lazy('meetings_list')
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Meeting'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the current user to the form
        return kwargs

    def form_valid(self, form):
        try:
            # Save the updated meeting
            meeting = form.save(commit=False)
            old_assigned_user = self.get_object().assigned_to
            new_assigned_user = form.cleaned_data.get('assigned_to')
            meeting.save()

            # Update MeetingAgenda if needed (if you have this requirement)
            delivery_unit = form.cleaned_data.get('delivery_unit')
            default_agenda = DeliveryUnitDefaultAgenda.objects.filter(
                delivery_unit=delivery_unit)
            if default_agenda.exists():
                MeetingAgenda.objects.filter(meeting=meeting).delete()
                meeting_agendas = [
                    MeetingAgenda(meeting=meeting, agenda=item.agenda)
                    for item in default_agenda
                ]
                MeetingAgenda.objects.bulk_create(meeting_agendas)

            # Handle role assignment if the assigned user is updated
            if new_assigned_user and new_assigned_user != old_assigned_user:
                participant_group = Group.objects.get(name='Participant')
                moderator_group = Group.objects.get(name='Moderator')

                # Update role for the old assigned user
                if old_assigned_user and old_assigned_user.groups.filter(name='Moderator').exists():
                    old_assigned_user.groups.remove(moderator_group)
                    old_assigned_user.groups.add(participant_group)

                # Update role for the new assigned user
                if new_assigned_user.groups.filter(name='Participant').exists():
                    new_assigned_user.groups.remove(participant_group)
                    new_assigned_user.groups.add(moderator_group)
            meeting_saved.send(sender=Meeting, instance=meeting, created=False)
            messages.success(self.request, 'Meeting Updated successfully.')
            return redirect(self.get_success_url())

        except Exception as e:
            print(e)
            messages.error(self.request, 'There was an error updating the meeting.')
            return self.form_invalid(form)

@method_decorator(has_permissions(['l3meetings.change_meeting']), name='dispatch')
class DeleteMeeting(LoginRequiredMixin, View):
    success_url = reverse_lazy('meetings_list')

    def post(self, request, *args, **kwargs):
        meeting = get_object_or_404(Meeting, pk=kwargs['pk'])
        assigned_user = meeting.assigned_to

        # Check if the current logged-in user is the assigned user
        if request.user != assigned_user:
            moderator_group = Group.objects.get(name='Moderator')
            participant_group = Group.objects.get(name='Participant')

            # Remove the 'Moderator' group and add the 'Participant' group
            if assigned_user.groups.filter(name='Moderator').exists():
                assigned_user.groups.remove(moderator_group)
                assigned_user.groups.add(participant_group)

        # Delete related agendas that are not default
        related_agendas = Agenda.objects.filter(
            meetingagenda__meeting=meeting, 
            is_default=False
        )

        for agenda in related_agendas:
            agenda.delete()

        # Delete related MeetingAgenda entries
        MeetingAgenda.objects.filter(meeting=meeting).delete()

        # Delete related action items
        ActionItem.objects.filter(meeting=meeting).delete()

        # Delete the meeting notes
        MeetingNotes.objects.filter(meeting=meeting).delete()

        # Delete the meeting itself
        meeting.delete()

        messages.success(request, 'The meeting and its related data were deleted successfully.')
        return HttpResponseRedirect(self.success_url)

@method_decorator(has_permissions(['l3meetings.change_meeting']), name='dispatch')
class MeetingActionItems(LoginRequiredMixin, TemplateView):
    model = ActionItem
    template_name = 'meetings/action-items.html'

    def get(self, request, *args, **kwargs):
        request.session['origin_url'] = request.path
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meeting = get_object_or_404(Meeting, pk=self.kwargs['pk'])
        context['page_title'] = 'Action Items'
        context['meeting_id'] = self.kwargs['pk']
        context['meetings'] = Meeting.objects.all().order_by('-id')
        context['action_items'] = ActionItem.objects.filter(
            meeting=meeting).order_by('-id')
        context['response_form'] = ResponseForm()
        return context

@method_decorator(has_permissions(['l3meetings.view_meeting']), name='dispatch')
class ActionItemIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'action-items/index.html'
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        request.session['origin_url'] = request.path
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Action Items'
        context['action_items'] = ActionItem.objects.all().order_by('-id')
        context['response_form'] = ResponseForm()
        context['is_close']   = "Close"
        return context

@method_decorator(has_permissions(['l3meetings.add_meeting']), name='dispatch')
class CreateActionItem(LoginRequiredMixin, FormView):
    template_name = 'action-items/create.html'
    form_class = ActionItemForm
    login_url = "/login/"

    def get_success_url(self):
        origin_url = self.request.session.get('origin_url')
        del self.request.session['origin_url']
        return origin_url

    def get_initial(self):
        initial = super().get_initial()
        initial['meeting'] = self.request.GET.get('meeting', '')
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Action Item'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        try:
            form.save()
            messages.success(self.request, 'Action Item Created successfully.')
        except Exception as e:
            messages.error(
                self.request, 'There was an error creating the action item.')
            return self.form_invalid(form)
        return super().form_valid(form)

@method_decorator(has_role(['Moderator']), name='dispatch')
@method_decorator(has_permissions(['l3meetings.change_meeting']), name='dispatch')
class UpdateActionItem(LoginRequiredMixin, UpdateView):
    model = ActionItem
    form_class = ActionItemForm
    template_name = 'action-items/edit.html'
    login_url = "/login/"

    def get_success_url(self):
        origin_url = self.request.session.get('origin_url')
        del self.request.session['origin_url']
        return origin_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(load_site_settings(self.request))
        context['form_title'] = 'Update Action Item'
        return context

    def form_valid(self, form):
        try:
            action_item = form.save(commit=False)
            if action_item.author is None:
                action_item.author = self.request.user
            else:
                if action_item.author.id != self.request.user.id and any(role in 'Moderator' for role in UserUtils.get_user_role(action_item.author_id)):
                    raise PermissionDenied("You do not have permission to update this Action Item.")

            action_item.save()
            is_email_sending_allowed = self.get_context_data()['allow_email_send']
            if action_item.assignedto:
                if is_email_sending_allowed == '1':
                    send_action_item_notification_email(action_item,'update')
            messages.success(self.request, 'Action Item updated successfully.')
            return super().form_valid(form)

        except PermissionDenied as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

        except Exception as e:
            messages.error(self.request, 'There was an error updating the action item.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error with the form. Please correct the errors and try again.')
        return redirect(self.get_success_url())

@method_decorator(has_permissions(['l3meetings.change_meeting']), name='dispatch')
class DeleteActionItem(LoginRequiredMixin, View):
    success_url = reverse_lazy('action_item_list')
    
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(ActionItem, pk=kwargs['pk'])
        obj.status = "close"
        obj.save()
        is_email_sending_allowed = load_site_settings(request)['allow_email_send']
        
        if is_email_sending_allowed == '1':
            send_action_item_notification_email(obj,'close')
        messages.success(request, 'The action item has been closed successfully.')
        return HttpResponseRedirect(self.success_url)

@method_decorator(has_permissions(['l3meetings.view_meeting']), name='dispatch')
class CurrentUserActionItems(LoginRequiredMixin, TemplateView):
    template_name = 'action-items/index.html'

    def get(self, request, *args, **kwargs):
        request.session['origin_url'] = request.path
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Action Items'
        context['action_items'] = ActionItem.objects.all().filter(
            assignedto=self.request.user).order_by('-id')
        context['response_form'] = ResponseForm()
        context['is_close'] = "Close"
        return context

@method_decorator(has_permissions(['l3meetings.add_agenda']), name='dispatch')
class AgendaIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'agendas/index.html'
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        request.session['origin_url'] = request.path
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Agendas'
        context['agendas'] = Agenda.objects.all().order_by("-is_default")
        return context

@method_decorator(has_permissions(['l3meetings.add_agenda']), name='dispatch')
class CreateAgendaView(LoginRequiredMixin, FormView):
    template_name = 'agendas/create.html'
    form_class = AgendaForm

    def get_success_url(self):
        origin_url = self.request.session.get('origin_url')
        del self.request.session['origin_url']
        return origin_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Agenda'
        meeting = Meeting.objects.get(slug=self.kwargs['slug'])
        context['meeting'] = meeting
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        try:
            agenda = form.save(commit=False)
            meeting_id = self.request.POST.get('meeting_id')
            meeting = Meeting.objects.get(id=meeting_id)

            agenda.save()
            MeetingAgenda.objects.create(meeting=meeting, agenda=agenda)

            messages.success(self.request, 'Agenda Created successfully.')
            return super().form_valid(form)
        except Meeting.DoesNotExist:
            messages.error(
                self.request, 'The specified meeting does not exist.')
            return self.form_invalid(form)
        except Exception as e:
            print(e)
            messages.error(
                self.request, 'There was an error creating the agenda.')
            return self.form_invalid(form)

@method_decorator(has_permissions(['l3meetings.add_response']), name='dispatch')
class AddResponseView(LoginRequiredMixin, FormView):
    form_class = ResponseForm
    success_url = reverse_lazy('action_item_list')
    login_url = "/login/"

    def form_valid(self, form):
        try:
            response = form.save(commit=False)
            response.responded_by = self.request.user
            obj = get_object_or_404(ActionItem, pk=response.action_item.id)
            obj.status = "inprogress"
            obj.save()
            response.save()
            messages.success(self.request, 'Action Response added successfully.')
            is_email_sending_allowed = load_site_settings(self.request)['allow_email_send']
            if is_email_sending_allowed == '1':
                send_action_item_notification_email(response.action_item, 'response')
        except Exception as e:
            messages.error(
                self.request, 'There was an error adding the response for action item.')
            return self.form_invalid(form)
        return super().form_valid(form)

@method_decorator(has_permissions(['l3meetings.view_response']), name='dispatch')
class ViewResponses(LoginRequiredMixin, TemplateView):
    template_name = 'partials/popups/view-responses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        action_item = get_object_or_404(ActionItem, pk=pk)
        responses = Response.objects.filter(
            action_item=action_item).select_related('action_item')
        context['action_item'] = action_item
        context['responses'] = responses
        return context

class CreateMeetingNotes(FormView):
    model = MeetingNotes
    form_class = MeetingNotesForm
    template_name = 'meetings/meeting_notes_form.html'
    success_url = reverse_lazy('meeting_notes_list')

class UpdateMeetingNotes(UpdateView):
    model = MeetingNotes
    form_class = MeetingNotesForm
    template_name = 'meetings/meeting_notes_form.html'
    success_url = reverse_lazy('meeting_notes_list')

class MeetingSchedulerView(FormView):
    form_class = ModeratorSelectionForm
    template_name = 'meetings/index.html'
    success_url = reverse_lazy('meetings_list')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        
        non_admin_users = User.objects.filter(is_staff=False)
        return form_class(users=non_admin_users, **self.get_form_kwargs())

    def get(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        context = self.get_context_data(form=form, meetings=Meeting.objects.all())
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
            new_moderator_id = form.cleaned_data['user'].id
            now = timezone.now()
            current_meetings = Meeting.objects.filter(meeting_date__lte=now)

            participant_group = Group.objects.get(name='Participant')
            moderator_group = Group.objects.get(name='Moderator')

            for current_meeting in current_meetings:
                if now.time() > current_meeting.meeting_date.time():
                    try:
                        current_moderator = current_meeting.assigned_to
                        if current_moderator:
                            if current_moderator.groups.filter(name='Moderator').exists():
                                current_moderator.groups.remove(moderator_group)
                                current_moderator.groups.add(participant_group)

                        new_moderator = User.objects.get(id=new_moderator_id)
                        new_meeting_date = self.get_next_meeting_date(current_meeting.meeting_date)

                        if not self.meeting_exists_for_month(new_meeting_date):
                            new_meeting = self.create_new_meeting(current_meeting, new_meeting_date, new_moderator_id)
                            self.copy_open_action_items_and_agendas(current_meeting, new_meeting)
                            meeting_saved.send(sender=Meeting, instance=new_meeting, created=True)
                            messages.success(request, f'Successfully scheduled next meeting: {new_meeting.title}')

                            if new_moderator.groups.filter(name='Participant').exists():
                                new_moderator.groups.remove(participant_group)
                                new_moderator.groups.add(moderator_group)
                        else:
                            messages.info(request, f'A meeting is already scheduled for the month of: {new_meeting_date.strftime("%B %Y")}')
                    except Exception as e:
                        messages.error(request, f'Error scheduling meeting for: {current_meeting.title}, Error: {e}')
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

    def get_next_meeting_date(self, current_date):
        holidays = get_holiday_dates()
        next_meeting_date = current_date + timedelta(days=30)
        while next_meeting_date.weekday() in (5, 6) or next_meeting_date in holidays:  # Skip weekends and holidays
            next_meeting_date += timedelta(days=1)
        return next_meeting_date

    def meeting_exists_for_month(self, date):
        first_day = date.replace(day=1)
        last_day = (first_day + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        return Meeting.objects.filter(meeting_date__range=[first_day, last_day]).exists()

    def create_new_meeting(self, current_meeting, new_meeting_date, new_moderator_id):
        next_month_suffix = new_meeting_date.strftime('%b %Y')
        context_data = load_site_settings(self.request)
        new_meeting = Meeting.objects.create(
            title           = f"{context_data['default_meeting_title']} - {next_month_suffix}",
            delivery_unit   = current_meeting.delivery_unit,
            meeting_date    = new_meeting_date,
            description     = current_meeting.description,
            assigned_to_id  = new_moderator_id
        )
        return new_meeting

    def copy_open_action_items_and_agendas(self, current_meeting, new_meeting):
        default_agenda = Agenda.objects.get(title="Open items of previous L3 Meeting", is_default=True)
        default_agendas = MeetingAgenda.objects.filter(meeting=current_meeting, agenda__is_default=True)
        for meeting_agenda in default_agendas:
            MeetingAgenda.objects.create(meeting=new_meeting, agenda=meeting_agenda.agenda)

        open_action_items = ActionItem.objects.filter(meeting=current_meeting, status='open')
        for item in open_action_items:
            item.meeting = new_meeting
            item.agenda = default_agenda
            item.save()
    

@method_decorator(has_permissions(['l3meetings.view_meeting']), name='dispatch')
class AttendanceIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance/index.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        request.session['origin_url'] = request.path
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Attendance'
        context['action_items'] = MeetingAttendance.objects.all().order_by('-first_name')
        context['response_form'] = ResponseForm()
        return context
