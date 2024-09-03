import datetime
from django.conf import settings
from sitesettings.models import SiteSettings

def load_site_settings(request=None):
    site_name = get_site_details('site_name')
    copyright_text = get_site_details('copyright_text')
    holidays = get_holiday_list()
    default_meeting_title = get_site_details('default_meeting_title')
    allow_email_send = get_site_details('allow_email_send')
    return {
        'site_name': site_name, 
        'holiday_list': holidays, 
        'copyright_text' : copyright_text,
        'default_meeting_title' : default_meeting_title,
        'allow_email_send' : allow_email_send,
    }

def get_site_details(setting_name=None):
    if setting_name is None:
        setting_name = 'site_name'
    details = SiteSettings.objects.get(key=setting_name).value
    return details


def get_holiday_list():
    holiday_list = SiteSettings.objects.get(key='holiday_list').value
    holiday_list = holiday_list.split(',')
    holidays = []
    year = datetime.datetime.now().year
    for holiday in holiday_list:
        holidays.append(str(year) + '-' + holiday.strip())
    holidays = ','.join(holidays)
    return holidays

def get_holiday_dates():
    holiday_list = SiteSettings.objects.get(key='holiday_list').value
    holiday_list = holiday_list.split(',')
    holidays = []
    year = datetime.datetime.now().year
    for holiday in holiday_list:
        holiday_date = datetime.datetime.strptime(f"{year}-{holiday.strip()}", "%Y-%m-%d").date()
        holidays.append(holiday_date)
    return holidays


def current_path(request):
    return {
        'current_path': request.path
    }