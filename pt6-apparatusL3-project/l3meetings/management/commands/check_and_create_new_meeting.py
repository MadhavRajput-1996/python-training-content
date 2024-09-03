import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from pytz import timezone as tz
from l3meetings.models import Meeting, ActionItem, MeetingAgenda, Agenda
from l3meetings.models import Meeting, ActionItem, MeetingAgenda
from signals import meeting_saved

logger = logging.getLogger(__name__)

# Define the timezone globally
local_tz = tz('Asia/Kolkata')

class Command(BaseCommand):
    help = 'Check for meetings that need a new meeting scheduled.'

    def handle(self, *args, **kwargs):
        now = timezone.now().astimezone(local_tz)  # Get the current time in Asia/Kolkata timezone
        logger.debug(f'Current local time: {now}')

        current_meetings = Meeting.objects.filter(meeting_date__lte=now)

        if current_meetings.exists():
            logger.debug(f'Found {current_meetings.count()} current meeting(s):')
        else:
            logger.debug('No current meetings found.')

        for current_meeting in current_meetings:
            if now.time() > current_meeting.meeting_date.time():
                try:
                    logger.debug(f'Processing meeting: {current_meeting.title}')
                    new_meeting_date = self.get_next_meeting_date(current_meeting.meeting_date)

                    # Check if a meeting is already scheduled for the same month
                    if not self.meeting_exists_for_month(new_meeting_date):
                        new_meeting = self.create_new_meeting(current_meeting, new_meeting_date)
                        self.copy_open_action_items_and_agendas(current_meeting, new_meeting)

                        # Trigger signal to handle invites
                        meeting_saved.send(sender=Meeting, instance=new_meeting, created=True)
                        logger.info(f'Successfully scheduled next meeting: {new_meeting.title}')
                    else:
                        logger.debug(f'A meeting is already scheduled for the month of: {new_meeting_date.strftime("%B %Y")}')
                except Exception as e:
                    logger.error(f'Error scheduling meeting for: {current_meeting.title}, Error: {e}')

    def get_next_meeting_date(self, current_date):
        try:
            current_date = current_date.astimezone(local_tz)
            next_meeting_date = current_date + timedelta(days=30)
            while next_meeting_date.weekday() in (5, 6):  # 5 = Saturday, 6 = Sunday
                next_meeting_date += timedelta(days=1)
            logger.debug(f'Next meeting date calculated: {next_meeting_date}')
            return next_meeting_date
        except Exception as e:
            logger.error(f'Error calculating next meeting date: {e}')
            raise

    def meeting_exists_for_month(self, date):
        try:
            # Determine the first and last day of the month for the given date
            first_day = date.replace(day=1)
            last_day = (first_day + timedelta(days=31)).replace(day=1) - timedelta(days=1)

            # Check if there are any meetings scheduled within this month
            return Meeting.objects.filter(meeting_date__range=[first_day, last_day]).exists()
        except Exception as e:
            logger.error(f'Error checking if meeting exists for month: {date.strftime("%B %Y")}, Error: {e}')
            raise

    def create_new_meeting(self, current_meeting, new_meeting_date):
        try:
            meeting_title = current_meeting.title.split(' - ')[0]
            next_month_suffix = new_meeting_date.strftime('%b %Y')
            new_title = f'{meeting_title} - {next_month_suffix}'

            new_meeting = Meeting.objects.create(
                title=new_title,
                delivery_unit=current_meeting.delivery_unit,
                meeting_date=new_meeting_date,
                description=current_meeting.description,
                assigned_to_id=current_meeting.assigned_to_id
            )
            logger.debug(f'New meeting created: {new_meeting.title}')
            return new_meeting
        except Exception as e:
            logger.error(f'Error creating new meeting: {e}')
            raise

    def copy_open_action_items_and_agendas(self, current_meeting, new_meeting):
        try:
            # Fetch the default agenda for "Open items of previous L3 Meeting"
            default_agenda = Agenda.objects.get(title="Open items of previous L3 Meeting", is_default=True)
            
            # Copy all default agendas from the current meeting to the new meeting
            default_agendas = MeetingAgenda.objects.filter(meeting=current_meeting, agenda__is_default=True)
            for meeting_agenda in default_agendas:
                MeetingAgenda.objects.create(meeting=new_meeting, agenda=meeting_agenda.agenda)
                logger.debug(f'Copied default agenda: {meeting_agenda.agenda.title} to new meeting: {new_meeting.title}')
            
            # Move all open action items from the current meeting to the new meeting
            open_action_items = ActionItem.objects.filter(meeting=current_meeting, status='open')
            for item in open_action_items:
                item.meeting = new_meeting
                item.agenda = default_agenda
                item.save()
                logger.debug(f'Moved action item: {item.title} to new meeting: {new_meeting.title} under default agenda: {default_agenda.title}')
            
        except Agenda.DoesNotExist:
            logger.error('Default agenda "Open items of previous L3 Meeting" not found.')
            raise
        except Exception as e:
            logger.error(f'Error copying action items and agendas: {e}')
            raise
