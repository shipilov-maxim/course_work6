from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            Group.objects.get(name="менеджер").delete()
        except Group.DoesNotExist:
            pass
        moderator = Group.objects.create(name="менеджер")
        moderator.permissions.set([24, 25, 41, 42],)
        moderator.save()
        try:
            User.objects.get(email='manager@manager.com').delete()
        except User.DoesNotExist:
            pass
        user = User.objects.create(
            email='manager@manager.com',
            first_name='Manager',
            last_name='Managerov',
            is_staff=True,
            is_active=True,
        )
        user.groups.set([moderator.pk])
        user.set_password('1234')
        user.save()
