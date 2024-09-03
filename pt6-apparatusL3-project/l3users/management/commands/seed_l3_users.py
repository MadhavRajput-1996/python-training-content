from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import receiver
from l3users.utils import DisableSignals
from sitesettings.context_processors import load_site_settings

class Command(BaseCommand):
    help = 'Seed the database with L3 users'

    def handle(self, *args, **kwargs):
        signals.post_save.disconnect(receiver=None, sender=User, dispatch_uid="my_id")

        self.stdout.write('Seeding L3 Users...')
        try:
            with DisableSignals(signals.post_save):
                l3_users = [
                    {
                        'username': 'kashyap.padh',
                        'email': 'kashyap.padh@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Kashyap',
                        'last_name': 'Padh'
                    },
                    {
                        'username': 'hemant.joshi',
                        'email': 'hemant.joshi@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Hemant',
                        'last_name': 'Joshi'
                    },
                    {
                        'username': 'amol.mahind',
                        'email': 'amol.mahind@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Amol',
                        'last_name': 'Mahind'
                    },
                    {
                        'username': 'sanjeet.patel',
                        'email': 'sanjeet.patel@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Sanjeet',
                        'last_name': 'Patel'
                    },
                    {
                        'username': 'vishnu.more',
                        'email': 'vishnu.more@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Vishnu',
                        'last_name': 'More'
                    },
                    {
                        'username': 'sandeep.gupta',
                        'email': 'sandeep.gupta@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Sandeep',
                        'last_name': 'Gupta'
                    },
                    {
                        'username': 'kiran.pyati',
                        'email': 'kiran.pyati@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Kiran',
                        'last_name': 'Pyati'
                    },
                    {
                        'username': 'hemant.joshi',
                        'email': 'hemant.joshi@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Hemant',
                        'last_name': 'Joshi'
                    },
                    {
                        'username': 'shivraj.singh',
                        'email': 'shivraj.singh@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'ShivrajSingh',
                        'last_name': 'Rawat'
                    },
                    {
                        'username': 'mayank.salunke',
                        'email': 'mayank.salunke@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Mayank',
                        'last_name': 'Salunke'
                    },
                    {
                        'username': 'sunil.talekar',
                        'email': 'sunil.talekar@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Sunil',
                        'last_name': 'Talekar'
                    },
                    {
                        'username': 'sourabh.tiwari',
                        'email': 'sourabh.tiwari@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Sourabh',
                        'last_name': 'Tiwari'
                    },
                    {
                        'username': 'kapil.yadav',
                        'email': 'kapil.yadav@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Kapil',
                        'last_name': 'Yadav'
                    },
                    {
                        'username': 'narendra.nagesh',
                        'email': 'narendra.nagesh@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Narendra',
                        'last_name': 'Nagesh'
                    },
                    {
                        'username': 'shashank.shroti',
                        'email': 'shashank.shroti@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Shashank',
                        'last_name': 'Shroti'
                    },
                    {
                        'username': 'abhijeet.dange',
                        'email': 'abhijeet.dange@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Abhijeet',
                        'last_name': 'Dange'
                    },
                    {
                        'username': 'vishal.mene',
                        'email': 'vishal.mene@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Vishal',
                        'last_name': 'Mene'
                    },
                    {
                        'username': 'mayank.salunke',
                        'email': 'mayank.salunke@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Mayank',
                        'last_name': 'Salunke'
                    },
                    {
                        'username': 'pankaj.nerkar',
                        'email': 'pankaj.nerkar@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Pankaj',
                        'last_name': 'Nerkar'
                    },
                    {
                        'username': 'sachin.yadav',
                        'email': 'sachin.yadav@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Sachin',
                        'last_name': 'Yadav'
                    },
                    {
                        'username': 'aaryaa.bhosale',
                        'email': 'aaryaa.bhosale@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Aaryaa',
                        'last_name': 'Bhosale'
                    },
                ]
                for u in l3_users:
                    user, created = User.objects.get_or_create(
                        username=u['username'],
                        defaults={
                            'email': u['email'],
                            'first_name': u['first_name'],
                            'last_name': u['last_name']
                        }
                    )
                    if not created:
                        User.objects.filter(username=u['username']).update(
                            email=u['email'],
                            first_name=u['first_name'],
                            last_name=u['last_name']
                        )
                    else:
                        user.set_password(u['password'])
                        user.save()
                    
                
                custom_admins = [
                    {
                        'username': 'amit.makhija',
                        'email': 'amit.makhija@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Amit',
                        'last_name': 'Makhija'
                    },
                    {
                        'username': 'jeevan.sharma',
                        'email': 'jeevan.sharma@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Jeevan',
                        'last_name': 'Sharma'
                    },
                    {
                        'username': 'pankaj.bothara',
                        'email': 'pankaj.bothara@infobeans.com',
                        'password': 'Info@123',
                        'first_name': 'Pankaj',
                        'last_name': 'Bothara'
                    },
                ]
                
                for u in custom_admins :
                    user, created = User.objects.get_or_create(
                        username=u['username'],
                        defaults={
                            'email'         : u['email'],
                            'first_name'    : u['first_name'],
                            'last_name'     : u['last_name'],
                            'is_staff'      : True,
                            'is_superuser'  : False,
                        }
                    )
                    if not created:
                        User.objects.filter(username=u['username']).update(
                            email           = u['email'],
                            first_name      = u['first_name'],
                            last_name       = u['last_name'],
                            is_staff        = True,
                            is_superuser    = False 
                        )
                    else:
                        user.set_password(u['password'])
                        user.save()
                    
            self.stdout.write(self.style.SUCCESS('Successfully seeded L3 Users.'))
            print(load_site_settings())
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding L3 Users: {str(e)}'))