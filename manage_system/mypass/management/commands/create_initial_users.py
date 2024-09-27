from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from mypass.models import UserProfile

class Command(BaseCommand):
    help = 'Create initial users with predefined usernames and passwords based on roles and sub-departments.'

    def handle(self, *args, **kwargs):
        # Predefined user data
        users_data = [
            {'username': 'employee_it1', 'password': 'employee123', 'role': 'Employee', 'sub_department': 'IT', 'institution': 'Default Institution'},
            {'username': 'depthead_it', 'password': 'depthead123', 'role': 'Department Head', 'sub_department': 'IT', 'institution': 'Default Institution'},
            {'username': 'employee_general1', 'password': 'employee123', 'role': 'Employee', 'sub_department': 'General Services', 'institution': 'Default Institution'},
            {'username': 'depthead_general', 'password': 'depthead123', 'role': 'Department Head', 'sub_department': 'General Services', 'institution': 'Default Institution'},
            {'username': 'employee_hr1', 'password': 'employee123', 'role': 'Employee', 'sub_department': 'HR', 'institution': 'Default Institution'},
            {'username': 'depthead_hr', 'password': 'depthead123', 'role': 'Department Head', 'sub_department': 'HR', 'institution': 'Default Institution'},
            {'username': 'employee_finance1', 'password': 'employee123', 'role': 'Employee', 'sub_department': 'Finance', 'institution': 'Default Institution'},
            {'username': 'depthead_finance', 'password': 'depthead123', 'role': 'Department Head', 'sub_department': 'Finance', 'institution': 'Default Institution'},
            {'username': 'employee_marketing1', 'password': 'employee123', 'role': 'Employee', 'sub_department': 'Marketing', 'institution': 'Default Institution'},
            {'username': 'depthead_marketing', 'password': 'depthead123', 'role': 'Department Head', 'sub_department': 'Marketing', 'institution': 'Default Institution'},
            {'username': 'security_head', 'password': 'security123', 'role': 'Security Head', 'sub_department': 'Security', 'institution': 'Default Institution'},
        ]

        for user_data in users_data:
            # Check if user already exists or create a new one
            user, created = User.objects.get_or_create(username=user_data['username'])
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                # Create UserProfile with the assigned role, sub-department, and institution
                UserProfile.objects.create(
                    user=user,
                    role=user_data['role'],
                    sub_department=user_data['sub_department'],
                    institution=user_data['institution']
                )
                self.stdout.write(self.style.SUCCESS(f"User '{user.username}' created successfully with role '{user_data['role']}' in '{user_data['sub_department']}' sub-department."))
            else:
                # Ensure UserProfile exists for the existing user
                if not UserProfile.objects.filter(user=user).exists():
                    UserProfile.objects.create(
                        user=user,
                        role=user_data['role'],
                        sub_department=user_data['sub_department'],
                        institution=user_data['institution']
                    )
                    self.stdout.write(self.style.SUCCESS(f"User '{user.username}' already existed, but UserProfile was missing and has been created."))
                else:
                    self.stdout.write(self.style.WARNING(f"User '{user.username}' already exists with a profile."))

        self.stdout.write(self.style.SUCCESS('Initial user creation process completed successfully.'))
