from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from mypass.models import UserProfile

class Command(BaseCommand):
    help = 'Create initial users with predefined usernames and passwords based on roles and sub-departments.'

    def handle(self, *args, **kwargs):
        # Predefined user data with department heads
        users_data = [
            {'username': 'employee_it1', 'password': 'employee123', 'role': 'Employee', 'sub_department': 'IT', 'institution': 'Default Institution'},
            {'username': 'depthead_it', 'password': 'depthead123', 'role': 'Department Head', 'sub_department': 'IT', 'institution': 'Default Institution', 'department_head_name': 'Mr. Prashath Sherigar'},
            {'username': 'employee_general1', 'password': 'employee123', 'role': 'Employee', 'sub_department': 'General Services', 'institution': 'Default Institution'},
            {'username': 'depthead_general', 'password': 'depthead123', 'role': 'Department Head', 'sub_department': 'General Services', 'institution': 'Default Institution', 'department_head_name': ' Basawaraj S Kuppasad'},
            {'username': 'employee_hr1', 'password': 'employee123', 'role': 'Employee', 'sub_department': 'HR', 'institution': 'Default Institution'},
            {'username': 'depthead_hr', 'password': 'depthead123', 'role': 'Department Head', 'sub_department': 'HR', 'institution': 'Default Institution', 'department_head_name': 'Ms.Akila S Poduval'},
            {'username': 'employee_finance1', 'password': 'employee123', 'role': 'Employee', 'sub_department': 'Finance', 'institution': 'Default Institution'},
            {'username': 'depthead_finance', 'password': 'depthead123', 'role': 'Department Head', 'sub_department': 'Finance', 'institution': 'Default Institution', 'department_head_name': 'Ms. Madhushri Hegde'},
            {'username': 'employee_marketing1', 'password': 'employee123', 'role': 'Employee', 'sub_department': 'Marketing', 'institution': 'Default Institution'},
            {'username': 'depthead_marketing', 'password': 'depthead123', 'role': 'Department Head', 'sub_department': 'Marketing', 'institution': 'Default Institution', 'department_head_name': 'Divya Dharshini K'},
            {'username': 'security_head', 'password': 'security123', 'role': 'Security Head', 'sub_department': 'Security', 'institution': 'Default Institution', 'department_head_name': 'Patrick Vas', 'security_head_name': 'Patrick Vas'},  # Add this line
        ]

        for user_data in users_data:
            # Check if user already exists or create a new one
            user, created = User.objects.get_or_create(username=user_data['username'])
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                # Create UserProfile with the assigned role, sub-department, and institution
                profile_data = {
                    'role': user_data['role'],
                    'sub_department': user_data['sub_department'],
                    'institution': user_data['institution'],
                }
                
                # Add department head name only for department heads
                if 'department_head_name' in user_data:
                    profile_data['department_head_name'] = user_data['department_head_name']
                
                UserProfile.objects.create(
                    user=user,
                    **profile_data
                )
                self.stdout.write(self.style.SUCCESS(f"User '{user.username}' created successfully with role '{user_data['role']}' in '{user_data['sub_department']}' sub-department."))
            else:
                # Ensure UserProfile exists for the existing user
                profile, created_profile = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'role': user_data['role'],
                        'sub_department': user_data['sub_department'],
                        'institution': user_data['institution'],
                    }
                )
                
                # Update profile with department head name if it's a department head
                if 'department_head_name' in user_data and profile.department_head_name is None:
                    profile.department_head_name = user_data['department_head_name']
                    profile.save()
                
                if created_profile:
                    self.stdout.write(self.style.SUCCESS(f"User '{user.username}' already existed, but UserProfile was missing and has been created."))
                else:
                    self.stdout.write(self.style.WARNING(f"User '{user.username}' already exists with a profile."))

        self.stdout.write(self.style.SUCCESS('Initial user creation process completed successfully.'))
