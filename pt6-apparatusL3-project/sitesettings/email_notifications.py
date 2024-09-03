# your_app/notifications.py

from django.core.mail import send_mail, BadHeaderError
from django.utils.html import strip_tags
from django.conf import settings
from sitesettings.models import EmailNotificationTemplate
from l3meetings.models import MeetingAgenda
import logging

logger = logging.getLogger(__name__)

def get_protocol():
    if getattr(settings, 'USE_HTTPS', False):
        return 'https://'
    else:
        return 'http://'

def send_action_item_notification_email(action_item, action_type):
    # Define template slugs based on action type
    template_slugs = {
        'create': 'action-item-added',
        'update': 'action-item-updated',
        'close': 'action-item-closed',
        'response': 'action-item-response'
    }

    # Get the appropriate template slug based on action type
    template_slug = template_slugs.get(action_type)

    if not template_slug:
        logger.error(f'Invalid action type: {action_type}')
        raise ValueError(f'Invalid action type: {action_type}')

    try:
        template = EmailNotificationTemplate.objects.get(slug=template_slug)
    except EmailNotificationTemplate.DoesNotExist:
        logger.error(f'Email template for action type "{action_type}" does not exist.')
        raise ValueError(f'Email template for action type "{action_type}" does not exist.')

    # Prepare email subject and recipient
    subject = template.subject.format(action_item_title=action_item.title)
    recipient_email = action_item.assignedto.email
    # Dynamic URL for the action item
    protocol = get_protocol()
    action_item_url = f"{protocol}{settings.CURRENT_DOMAIN}/meetings/action-items/"
    # Format the email template with actual data
    html_message = template.body.format(
        recipient_name=action_item.assignedto.first_name,
        action_item_title=action_item.title,
        action_item_link=action_item_url,
        action_item_agenda=action_item.agenda.title if action_item.agenda else '',
        start_date=action_item.start_date.strftime('%Y-%m-%d'),  # Format date
        target_end_date=action_item.target_end_date.strftime('%Y-%m-%d'),
        updated_by_name=action_item.author.first_name,
        status=action_item.status,
        sender_name=settings.EMAIL_HOST_USER,
        site_link=settings.CURRENT_DOMAIN
    )
    
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER

    try:
        send_mail(subject, plain_message, from_email, [recipient_email], fail_silently=False, html_message=html_message)
    except BadHeaderError:
        logger.error(f'Invalid header found while sending email to {recipient_email}')
        raise ValueError('Invalid header found.')
    except Exception as e:
        logger.error(f'Error sending email to {recipient_email}: {str(e)}')
        raise e
    

def send_meeting_invitation_email(meeting, recipient_users):
    try:
        # Fetch the meeting invitation template
        template = EmailNotificationTemplate.objects.get(slug='meeting-invitation')
    except EmailNotificationTemplate.DoesNotExist:
        logger.error('Meeting invitation email template does not exist.')
        raise ValueError('Meeting invitation email template does not exist.')
    if not recipient_users:
        logger.info('No non-admin users found to send invites.')
        return

    # Build the agenda items list
    agenda_items = MeetingAgenda.objects.filter(meeting=meeting)
    agenda_list_html = ''.join([f"<li>{agenda.agenda.title}</li>" for agenda in agenda_items])

    # Prepare email subject and body
    subject = template.subject.format(meeting_title=meeting.title)
    html_message = template.body.format(
        recipient_name="{recipient_name}",
        meeting_title=meeting.title,
        meeting_description=meeting.description,
        meeting_date=meeting.meeting_date.strftime('%Y-%m-%d'),
        meeting_time=meeting.meeting_date.strftime('%H:%M'),
        meeting_agenda_items=agenda_list_html,
        sender_name=settings.EMAIL_HOST_USER
    )

    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER

    for user in recipient_users:
        personalized_html_message = html_message.format(recipient_name=user.first_name)
        try:
            send_mail(
                subject,
                plain_message,
                from_email,
                [user.email],
                fail_silently=False,
                html_message=personalized_html_message,
            )
        except BadHeaderError:
            logger.error(f'Invalid header found while sending email to {user.email}')
            raise ValueError('Invalid header found.')
        except Exception as e:
            logger.error(f'Error sending email to {user.email}: {str(e)}')
            raise e

def send_meeting_update_email(meeting, recipient_users):
    try:
        # Fetch the meeting update template
        template = EmailNotificationTemplate.objects.get(slug='meeting-update')
    except EmailNotificationTemplate.DoesNotExist:
        logger.error('Meeting update email template does not exist.')
        raise ValueError('Meeting update email template does not exist.')
    
    if not recipient_users:
        logger.info('No non-admin users found to send update notifications.')
        return

    # Build the agenda items list
    agenda_items = MeetingAgenda.objects.filter(meeting=meeting)
    agenda_list_html = ''.join([f"<li>{agenda.agenda.title}</li>" for agenda in agenda_items])

    # Prepare email subject and body
    subject = template.subject.format(meeting_title=meeting.title)
    html_message = template.body.format(
        recipient_name="{recipient_name}",
        meeting_title=meeting.title,
        meeting_description=meeting.description,
        meeting_date=meeting.meeting_date.strftime('%Y-%m-%d'),
        meeting_time=meeting.meeting_date.strftime('%H:%M'),
        meeting_agenda_items=agenda_list_html,
        sender_name=settings.EMAIL_HOST_USER
    )

    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER

    for user in recipient_users:
        personalized_html_message = html_message.format(recipient_name=user.first_name)
        try:
            send_mail(
                subject,
                plain_message,
                from_email,
                [user.email],
                fail_silently=False,
                html_message=personalized_html_message,
            )
        except BadHeaderError:
            logger.error(f'Invalid header found while sending update email to {user.email}')
            raise ValueError('Invalid header found.')
        except Exception as e:
            logger.error(f'Error sending update email to {user.email}: {str(e)}')
            raise e


