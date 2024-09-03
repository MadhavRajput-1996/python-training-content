from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.core.mail import send_mail, BadHeaderError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.core.management import call_command
from django.conf import settings
import logging
from django.apps import AppConfig
from l3meetings.models import ActionItem, Meeting, Response, MeetingAgenda, MeetingAttendance
from invites.models import MeetingInvites
from sitesettings.email_notifications import send_meeting_invitation_email,send_meeting_update_email
from sitesettings.context_processors import load_site_settings

MOD_MODELS = [ActionItem, Meeting, Response]
PT_MODELS = [ActionItem, Meeting, Response]

logger = logging.getLogger(__name__)

meeting_saved = Signal()

@receiver(post_migrate)
def run_seeders(sender, **kwargs):
    call_command('seed_groups')
    call_command('seed_default_agendas')
    call_command('seed_delivery_units')
    call_command('seed_delivery_unit_default_agendas')
    call_command('seed_google_credentails_admin_side')
    call_command('seed_l3_users')


@receiver(post_migrate)
def assign_permissions_to_group(sender, **kwargs):
    group, created = Group.objects.get_or_create(name='Moderator')

    for model in MOD_MODELS:
        content_type = ContentType.objects.get_for_model(model)

        # Define the permissions you want to assign
        permissions = Permission.objects.filter(content_type=content_type)

        # Add permissions to the group if not already assigned
        for permission in permissions:
            if not group.permissions.filter(id=permission.id).exists():
                group.permissions.add(permission)
                print(
                    f"Assigned permission '{permission.codename}' for {model.__name__} to group {group.name}")


@receiver(post_migrate)
def assign_permissions_to_group_participant(sender, **kwargs):
    group, created = Group.objects.get_or_create(name='Participant')

    for model in PT_MODELS:
        content_type = ContentType.objects.get_for_model(model)

        # Define the view permissions you want to assign
        permissions = Permission.objects.filter(
            content_type=content_type, codename__startswith='view_')

        # Add permissions to the group if not already assigned
        for permission in permissions:
            if not group.permissions.filter(id=permission.id).exists():
                group.permissions.add(permission)
                print(
                    f"Assigned permission '{permission.codename}' for {model.__name__} to group {group.name}")


@receiver(meeting_saved)
def post_save_create_invite_receiver(sender, instance, created, **kwargs):
    if created:
        try:
            non_admin_users = User.objects.filter(is_staff=False, is_superuser=False)
            if not non_admin_users.exists():
                logger.info('No non-admin users found to send invites.')
                return

            invite_emails = list(non_admin_users.values_list('email', flat=True))
            invite_emails_str = ','.join(invite_emails)

            for user in non_admin_users:
                attendance = MeetingAttendance(
                    meeting=instance,
                    user=user,
                    is_present=False
                )
                attendance.save()
                
            meeting_invite = MeetingInvites(
                meeting=instance,
                invitees=invite_emails_str,
            )
            meeting_invite.save()
            allow_email_send = load_site_settings()
            allow_email_send = allow_email_send['allow_email_send']
            
            # Send invite emails
            if allow_email_send == '1':
                send_meeting_invitation_email(meeting=instance, recipient_users=non_admin_users)
        except BadHeaderError:
            logger.error('Invalid header found in the email.')
        except ObjectDoesNotExist as e:
            logger.error(f"Object does not exist: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            
    else:
        # Handle meeting update logic
        try:
            logger.info(f'Meeting "{instance.title}" was updated.')
            non_admin_users = User.objects.filter(is_staff=False, is_superuser=False)
            allow_email_send = load_site_settings()
            allow_email_send = allow_email_send['allow_email_send']
            
            # Send invite emails
            if allow_email_send == '1':
                send_meeting_update_email(meeting=instance, recipient_users=non_admin_users)

        except BadHeaderError:
            logger.error('Invalid header found in the email.')
        except ObjectDoesNotExist as e:
            logger.error(f"Object does not exist: {e}")
        except Exception as e:
            logger.error(f"An error occurred while updating the meeting: {e}")        
