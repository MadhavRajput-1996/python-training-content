# accounts/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.core.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from allauth.account.utils import perform_login
from allauth.utils import get_user_model
from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
from django.conf import settings
from allauth.account.models import EmailAddress
from django.contrib.auth.models import Group
from .models import UserProfileInfo


class MyAccountAdapter(DefaultAccountAdapter):
    def add_message(self, request, level, message_template, message_context=None, extra_tags=''):
        if message_template != 'account/messages/logged_in.txt':
            super().add_message(request, level, message_template, message_context, extra_tags)



class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Restrict login to infobeans.com domain
        email = sociallogin.account.extra_data.get('email', '')
        allowed_domains = ['infobeans.com']  # List of allowed email domains
        domain = email.split('@')[-1] if '@' in email else None

        # if domain not in allowed_domains:
        #     raise ImmediateHttpResponse(
        #         redirect(reverse('login') + '?domain_error=1')
        #     )

        # Handle first-time Google login
        user = sociallogin.user
        if not user.id:
            try:
                existing_user = get_user_model().objects.get(email=user.email)
                perform_login(request, existing_user, email_verification=False)
                raise ImmediateHttpResponse(redirect('/'))
            except get_user_model().DoesNotExist:
                pass

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        # Save additional profile info for first-time Google login
        if sociallogin.account.provider == 'google':
            extra_data = sociallogin.account.extra_data
            # Save profile picture if available
            if 'picture' in extra_data:
                profile_pic_url = extra_data['picture']
                profile_info = UserProfileInfo.objects.get_or_create(user=user)[0]
                profile_info.profile_pic = profile_pic_url
                profile_info.save()

            # Save phone number if available
            if 'phone' in extra_data:
                phone_number = extra_data['phone']
                profile_info.phone = phone_number
                
                profile_info.save()

            # Assign default role 'Participant' if first-time login via Google
            #if not EmailAddress.objects.filter(user=user, verified=True).exists():
            participant_group = Group.objects.get(name='Participant')
            user.groups.add(participant_group)
            profile_info.group = participant_group
            profile_info.save()

        return user