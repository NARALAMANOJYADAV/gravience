from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User


class Command(BaseCommand):
    help = 'Create groups (counselor, class_incharge, hod, director) and example users'

    def handle(self, *args, **options):
        groups = ['counselor', 'class_incharge', 'hod', 'director']
        for g in groups:
            group, created = Group.objects.get_or_create(name=g)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {g}'))
            else:
                self.stdout.write(self.style.NOTICE(f'Group exists: {g}'))

        # create example users with known passwords only if they don't exist
        examples = [
            ('counselor_user', 'counselor', 'counselor123'),
            ('incharge_user', 'class_incharge', 'incharge123'),
            ('hod_user', 'hod', 'hod123'),
            ('director_user', 'director', 'director123'),
        ]
        for username, group_name, pwd in examples:
            if not User.objects.filter(username=username).exists():
                u = User.objects.create_user(username=username, password=pwd)
                g = Group.objects.get(name=group_name)
                u.groups.add(g)
                u.save()
                self.stdout.write(self.style.SUCCESS(f'Created user {username} in group {group_name}'))
            else:
                self.stdout.write(self.style.NOTICE(f'User {username} already exists'))

        # ensure admin superuser exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin (password: admin123)'))
        else:
            self.stdout.write(self.style.NOTICE('Admin user already exists'))
