from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class DeliveryUnit(models.Model):
    title = models.CharField(max_length=250, unique=True)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.title


class Meeting(models.Model):

    title = models.CharField(max_length=250, unique=True)
    description = models.TextField(max_length=250)
    meeting_date = models.DateTimeField()
    delivery_unit = models.ForeignKey(DeliveryUnit, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_superuser': False})
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class MeetingNotes(models.Model):

    note_description = RichTextField()
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Meeting Notes"

    def __str__(self):
        return self.note_description



class Agenda(models.Model):

    status_choices = (
        ('open', 'Open'),
        ('close', 'Close'),
    )

    title = models.CharField(max_length=70)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    status = models.CharField(
        max_length=10,
        choices=status_choices,
        default='open'
    )

    class Meta:
        verbose_name = "Agenda"
        verbose_name_plural = "Agendas"

    def __str__(self):
        return self.title

    @property
    def created_by_first_name(self):
        return self.created_by.first_name if self.created_by else ''


class ActionItem(models.Model):

    status_choices = (
        ('open', 'Open'),
        ('close', 'Close'),
        ('inprogress', 'In-Progress'),
    )

    assignedto = models.ForeignKey(
        User, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    start_date = models.DateTimeField()
    target_end_date = models.DateTimeField()
    actual_end_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE, related_name='author')
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=10,
        choices=status_choices,
        default='open'
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.author is None and 'current_user' in kwargs:
            self.author = kwargs.pop('current_user')
        super().save(*args, **kwargs)


class DeliveryUnitDefaultAgenda(models.Model):
    delivery_unit = models.ForeignKey(DeliveryUnit, on_delete=models.CASCADE)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Delivery Unit Default Agenda"

    def __str__(self):
        return self.delivery_unit.title+' => '+self.agenda.title


class MeetingAgenda(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Meeting Agenda"

    def __str__(self):
        return self.meeting.title+' => '+self.agenda.title

class Response(models.Model):
    action_item = models.ForeignKey(ActionItem, on_delete=models.CASCADE)
    response_date = models.DateTimeField(default=timezone.now)
    responded_by = models.CharField(max_length=100)
    response_text = models.TextField()

    def __str__(self):
        return f"Response by {self.responded_by} on {self.response_date}"
    

class MeetingAttendance(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)