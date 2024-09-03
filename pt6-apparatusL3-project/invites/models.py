from django.db import models
from l3meetings.models import Meeting
from ckeditor.fields import RichTextField

# Create your models here.
class MeetingInvites(models.Model):
    meeting = models.OneToOneField(Meeting, on_delete=models.CASCADE)
    # invite_details = models.TextField(max_length=300, null=True)
    invite_details = RichTextField()
    invitees = models.TextField(null=False, default='')

    def __str__(self):
        return f"Schedule for Meeting: {self.meeting.title}"
