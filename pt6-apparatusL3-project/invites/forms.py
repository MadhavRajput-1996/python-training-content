from django import forms
from .models import MeetingInvites
from l3meetings.models import Meeting
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget

class MeetingsScheduleForm(forms.ModelForm):
    meeting = forms.ModelChoiceField(queryset=Meeting.objects.all(), required=True)
    meeting_date = forms.DateField(required=True)
    invite_details = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = MeetingInvites
        fields = [
            'meeting',
            'invite_details',
            'meeting_date',
            'invitees',
        ]
    
    def clean(self):
        cleaned_data = super().clean()
        meeting = cleaned_data.get('meeting')
        invitees = cleaned_data.get('invitees')
        edit_mode = self.instance.pk is not None

        if not edit_mode:
            if meeting and MeetingInvites.objects.filter(meeting=meeting).exists():
                self.add_error('meeting', 'This meeting is already scheduled.')
        
        if invitees:
            invitees_list = invitees.split(',')
            invalid_emails = []
            for invitee in invitees_list:
                invitee = invitee.strip()
                try:
                    validate_email(invitee)
                except ValidationError:
                    invalid_emails.append(invitee)
            
            if invalid_emails:
                self.add_error('invitees', f'These emails are invalid: {", ".join(invalid_emails)}')
        
        return cleaned_data

    def __init__(self, *args, pk=None, **kwargs):
        super(MeetingsScheduleForm, self).__init__(*args, **kwargs)
        meeting_id = pk

        if self.instance.pk:
            self.fields['meeting'].initial = self.instance.meeting
            self.fields['meeting'].queryset = Meeting.objects.filter(pk=self.instance.meeting.id)
            self.fields['meeting'].widget.attrs.update({'readonly': 'true'})
            self.fields['meeting_date'].initial = self.instance.meeting.meeting_date
        else:
            if meeting_id:
                meeting = Meeting.objects.get(id=meeting_id)
                self.fields['meeting'].initial = meeting
                self.fields['meeting'].queryset = Meeting.objects.filter(pk=meeting_id)
                self.fields['meeting'].widget.attrs.update({'readonly': 'true'})
                self.fields['meeting_date'].initial = meeting.meeting_date
            else:
                self.fields['meeting'].queryset = Meeting.objects.exclude(meetingschedule__isnull=False)
        
        for field_name, field in self.fields.items():
            if field_name == 'meeting_date':
                field.widget.attrs.update({'class': 'form-control datepicker'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
    
    
    def save(self, commit=True):
        instance = super().save(commit=True)
        if instance.meeting:
            instance.meeting.meeting_date = self.cleaned_data['meeting_date']
            if commit:
                instance.meeting.save()
        return instance

