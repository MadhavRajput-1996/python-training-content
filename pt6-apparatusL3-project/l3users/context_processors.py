from .models import UserProfileInfo
from django.conf import settings
from allauth.socialaccount.models import SocialApp

def user_profile(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfileInfo.objects.get(user=request.user)
        except UserProfileInfo.DoesNotExist:
            profile = None
        return {'user_profile': profile}
    return {}


def social_apps_status(request):
    context = {}
    google_app = SocialApp.objects.filter(provider='google').first()
    context['google_social_app_configured'] = google_app is not None
    return context
