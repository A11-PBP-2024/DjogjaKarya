from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a default admin account if not exists'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin', 
                password='admindjogjakarya', 
                email='admin@djogjakarya.id'
            )
            self.stdout.write(self.style.SUCCESS('Admin account created successfully.'))
        else:
            self.stdout.write('Admin account already exists.')
