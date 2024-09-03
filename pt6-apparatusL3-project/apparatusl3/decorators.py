from functools import wraps
from django.core.exceptions import PermissionDenied


def has_permissions(required_permissions):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_permissions = request.user.get_all_permissions()
            if any(perm in user_permissions for perm in required_permissions):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied(
                "You do not have permission to access this resource.")
        return _wrapped_view
    return decorator


def has_role(required_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_groups = request.user.groups.values_list('name', flat=True)
            if request.user.is_superuser or any(role in user_groups for role in required_roles):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied("You do not have permission to access this resource.")
        return _wrapped_view
    return decorator
