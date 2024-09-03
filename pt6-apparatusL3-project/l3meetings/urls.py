from django.urls import path
from .views import *

urlpatterns = [
    path('', MeetingIndexView.as_view(), name='meetings_list'),
    path('<slug:slug>', MeetingDetailView.as_view(), name='meeting_detail'),
    path('create/', CreateMeeting.as_view(), name='create_meeting'),
    path('<int:pk>/edit', UpdateMeeting.as_view(), name='update_meeting'),
    path('<int:pk>/delete', DeleteMeeting.as_view(), name='delete_meeting'),
    path('<int:pk>/action-items', MeetingActionItems.as_view(), name='meeting_action_items'),
    path('agenda/<int:pk>/update/', UpdateAgenda.as_view(), name="update_agenda"),
    path('agendas', AgendaIndexView.as_view(), name='agendas_list'),
    path('<slug:slug>/agenda/create/', CreateAgendaView.as_view(), name='create_agenda'),
    path('action-items/', ActionItemIndexView.as_view(), name='action_item_list'),
    path('my-action-items/', CurrentUserActionItems.as_view(), name='current_user_action_item_list'),
    path('action-items/create/', CreateActionItem.as_view(), name='create_actionitem'),
    path('action-items/<int:pk>/edit', UpdateActionItem.as_view(), name='update_actionitem'),
    path('action-items/<int:pk>/delete', DeleteActionItem.as_view(), name='delete_actionitem'),
    path('action-item/responses/<int:pk>/add', AddResponseView.as_view(), name='add_response'),
    path('action-item/responses/<int:pk>/view/', ViewResponses.as_view(), name='view_responses'),
    path('meeting-notes/create/', CreateMeetingNotes.as_view(), name='create_meeting_notes'),
    path('meeting-notes/<int:pk>/edit/', UpdateMeetingNotes.as_view(), name='edit_meeting_notes'),
    path('schedule/', MeetingSchedulerView.as_view(), name='schedule_meeting'),
]
