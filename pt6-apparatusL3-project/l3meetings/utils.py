from django.contrib.auth.models import User
from sitesettings.models import SiteSettings

class UserUtils:
    @classmethod
    def get_user_role(cls, user_id):
        try:
            user = User.objects.get(id=user_id)
            user_groups = user.groups.values_list('name', flat=True)
            return user_groups
        except User.DoesNotExist:
            return None
