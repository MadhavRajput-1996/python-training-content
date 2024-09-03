from django import forms
from .models import ActionItem, Meeting, Response, Agenda,MeetingNotes, MeetingAttendance
from django.contrib.auth.models import User
from .fields import UserModelChoiceField
from django.db.models.functions import Lower
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget
from django.utils.timezone import now, localtime
from calendar import monthrange

class UserChoiceSelection(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name.capitalize()} {obj.last_name.capitalize()} ({obj.email})"

class MeetingForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Meeting
        fields = [
            'title',
            'description',
            'meeting_date',
            'delivery_unit',
            'assigned_to',
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        context_data = kwargs.pop('context_data', {})
        super(MeetingForm, self).__init__(*args, **kwargs)
        self.fields['delivery_unit'].initial = '1'
        self.fields['assigned_to'] = UserChoiceSelection(queryset=User.objects.filter(is_superuser=False))
        self.fields['title'].initial = f"{context_data.get('default_meeting_title', '')} - {now().strftime('%b %Y')}"
        self.fields['title'].widget.attrs.update({'readonly': 'readonly'})
        if self.user:
            self.fields['assigned_to'].initial = self.user.id
                    
        for field_name, field in self.fields.items():
            if field_name == 'meeting_date':
                field.widget.attrs.update({'class': 'form-control datepicker'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean_meeting_date(self):
        meeting_date = self.cleaned_data.get('meeting_date')
        is_valid_meeting_date = meeting_date
        if hasattr(is_valid_meeting_date, 'date'):
            is_valid_meeting_date = is_valid_meeting_date.date()
        today = now().date()

        # Calculate the start and end of the valid date range
        start_date = today.replace(day=1)
        
        # Get the year and month two months from now
        if today.month == 12:
            next_month = 1
            next_year = today.year + 1
        else:
            next_month = today.month + 2
            next_year = today.year

        last_day_next_month = monthrange(next_year, next_month)[1]
        end_date = today.replace(year=next_year, month=next_month, day=last_day_next_month)

        # Check if the is_valid_meeting_date is within the valid range
        if not (start_date <= is_valid_meeting_date <= end_date):
            raise forms.ValidationError(f"Meeting dates must be between {start_date.strftime('%b-%Y')} and {end_date.strftime('%b-%Y')}.")

        if is_valid_meeting_date.weekday() >= 5:  # Saturday is 5 and Sunday is 6
            raise forms.ValidationError("Meetings cannot be scheduled for weekends (Saturday or Sunday).")
        return meeting_date
    
    def save(self, commit=True):
        meeting = super(MeetingForm, self).save(commit=False)
        meeting_date = self.cleaned_data.get('meeting_date')
        meeting_month_year = localtime(meeting_date).strftime('%b %Y')
        
        # Remove any existing month-year suffix from the title
        # if "-" in meeting.title:
        #     meeting_title = meeting.title.rsplit(" - ", 1)[0]
        # else:
        #     meeting_title = meeting.title
        # # Update the title to include the new month-year suffix
        # meeting.title = f"{meeting_title} - {meeting_month_year}"
        
        if not meeting.assigned_to:
            meeting.assigned_to = self.user
        if commit:
            meeting.save()
        return meeting

class ActionItemForm(forms.ModelForm):
    required_css_class = 'required'
    assignedto = UserModelChoiceField(queryset=User.objects.order_by(
        Lower('first_name'), Lower('last_name')))

    class Meta:
        model = ActionItem
        fields = [
            'title',
            'assignedto',
            'start_date',
            'target_end_date',
            'actual_end_date',
            'status',
            'meeting'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ActionItemForm, self).__init__(*args, **kwargs)

        # Filter out admin users and create a list of choices
        users =  User.objects.filter(is_superuser=False).order_by(Lower('first_name'), Lower('last_name'))

        # Get one superuser for All option value.
        superUsr = User.objects.filter(is_superuser=True).values()
        if superUsr:
            user_choices = [(superUsr[0]['id'], 'All')] + [(user.id, f'{user.first_name} {user.last_name}') for user in users]
            # Assign the choices to the assignedto field
            self.fields['assignedto'].choices = user_choices

        for field_name in ['meeting']:
            self.fields[field_name].choices = [
                ('', '')] + list(self.fields[field_name].choices)[1:]

        for field_name, field in self.fields.items():
            if field_name in ['start_date', 'target_end_date', 'actual_end_date']:
                field.widget.attrs.update({'class': 'form-control datepicker'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

        self.fields['assignedto'].initial = user

class ResponseForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Response
        fields = ['action_item', 'response_date', 'response_text']
        widgets = {
            'response_text': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['action_item'].widget.attrs.update({
            'class': 'form-control p-event-none has-value',
            'id': 'id_action_item',

        })

        self.fields['response_text'].widget.attrs.update(
            {'placeholder': '', 'class': 'form-control'})
        self.fields['response_date'].widget.attrs.update(
            {'placeholder': '', 'class': 'form-control datepicker'})

class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = [
            'title',
            'created_by',
            'status'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AgendaForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['created_by'].initial = user

class MeetingNotesForm(forms.ModelForm):
    note_description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = MeetingNotes
        fields = ['note_description']
        widgets = {
            'note_description': CKEditorWidget(),
            'meeting': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(MeetingNotesForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'note_description':
                field.widget.attrs.update({'class': 'form-control'})
                
class ModeratorSelectionForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=False),
        label="Select Moderator",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        users = kwargs.pop('users', User.objects.none())
        super().__init__(*args, **kwargs)
        self.fields['user'].choices = [
            (user.id, f"{user.first_name} {user.last_name}")
            for user in users
        ]
        
        
class MeetingAttendanceForm(forms.ModelForm):
    absent_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.SelectMultiple(attrs={'size': '20', 'class': 'form-control'}),
        required=False
    )
    present_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.SelectMultiple(attrs={'size': '20', 'class': 'form-control'}),
        required=False
    )
    class Meta:
        model = MeetingAttendance
        fields = []

    def __init__(self, *args, **kwargs):
        meeting = kwargs.pop('meeting')
        super().__init__(*args, **kwargs)
        meeting_users = User.objects.filter(meetingattendance__meeting=meeting)

        absent_users_qs = meeting_users.filter(meetingattendance__is_present=False).order_by('first_name')
        present_users_qs = meeting_users.filter(meetingattendance__is_present=True).order_by('first_name')

        self.fields['absent_users'].choices = [(user.id, f"{user.first_name} {user.last_name}") for user in absent_users_qs]
        self.fields['present_users'].choices = [(user.id, f"{user.first_name} {user.last_name}") for user in present_users_qs]
