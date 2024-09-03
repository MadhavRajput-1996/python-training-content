def has_add_meeting_schedule_permission(request):
    if request.user.is_authenticated:
        return request.user.has_perm('invites.add_meetingschedule')
    return False

#add permissions to check in the list.
def user_permission_context(request):
    context = {}
    context['has_add_meeting_schedule_permission'] = has_add_meeting_schedule_permission(request)
    return context